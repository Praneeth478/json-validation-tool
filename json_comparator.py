"""
JSON Comparator module for deep comparison of JSON objects.
Provides functionality similar to Beyond Compare for JSON data.
"""

from typing import Any, Dict, List, Union, Optional
from enum import Enum


class ChangeType(str, Enum):
    """Types of changes detected in JSON comparison."""
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    TYPE_CHANGED = "type_changed"


class Difference:
    """Represents a single difference between two JSON objects."""
    
    def __init__(self, path: str, change_type: ChangeType, 
                 old_value: Any = None, new_value: Any = None, 
                 old_type: Optional[str] = None, new_type: Optional[str] = None):
        self.path = path
        self.change_type = change_type
        self.old_value = old_value
        self.new_value = new_value
        self.old_type = old_type
        self.new_type = new_type
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert difference to dictionary format."""
        result = {
            "path": self.path,
            "change_type": self.change_type.value,
        }
        
        if self.change_type == ChangeType.ADDED:
            result["new_value"] = self.new_value
            result["new_type"] = type(self.new_value).__name__
        elif self.change_type == ChangeType.REMOVED:
            result["old_value"] = self.old_value
            result["old_type"] = type(self.old_value).__name__
        elif self.change_type == ChangeType.MODIFIED:
            result["old_value"] = self.old_value
            result["new_value"] = self.new_value
            result["old_type"] = type(self.old_value).__name__
            result["new_type"] = type(self.new_value).__name__
        elif self.change_type == ChangeType.TYPE_CHANGED:
            result["old_value"] = self.old_value
            result["new_value"] = self.new_value
            result["old_type"] = self.old_type
            result["new_type"] = self.new_type
        
        return result


class JSONComparator:
    """Main class for comparing JSON objects."""
    
    def __init__(self, ignore_order: bool = False, ignore_case: bool = False):
        """
        Initialize the JSON comparator.
        
        Args:
            ignore_order: If True, ignore order of items in lists
            ignore_case: If True, ignore case when comparing strings
        """
        self.ignore_order = ignore_order
        self.ignore_case = ignore_case
        self.differences: List[Difference] = []
    
    def compare(self, obj1: Any, obj2: Any) -> List[Difference]:
        """
        Compare two JSON objects and return list of differences.
        
        Args:
            obj1: First JSON object
            obj2: Second JSON object
            
        Returns:
            List of Difference objects
        """
        self.differences = []
        self._deep_compare(obj1, obj2, "")
        return self.differences
    
    def _deep_compare(self, obj1: Any, obj2: Any, path: str):
        """Recursively compare two objects."""
        
        # Handle None values
        if obj1 is None and obj2 is None:
            return
        elif obj1 is None:
            self.differences.append(Difference(path, ChangeType.ADDED, None, obj2))
            return
        elif obj2 is None:
            self.differences.append(Difference(path, ChangeType.REMOVED, obj1, None))
            return
        
        # Check if types are different
        if type(obj1) != type(obj2):
            self.differences.append(Difference(
                path, ChangeType.TYPE_CHANGED, obj1, obj2,
                type(obj1).__name__, type(obj2).__name__
            ))
            return
        
        # Compare based on type
        if isinstance(obj1, dict):
            self._compare_dicts(obj1, obj2, path)
        elif isinstance(obj1, list):
            self._compare_lists(obj1, obj2, path)
        else:
            self._compare_primitives(obj1, obj2, path)
    
    def _compare_dicts(self, dict1: Dict, dict2: Dict, path: str):
        """Compare two dictionaries."""
        all_keys = set(dict1.keys()) | set(dict2.keys())
        
        for key in all_keys:
            new_path = f"{path}.{key}" if path else str(key)
            
            if key not in dict1:
                self.differences.append(Difference(new_path, ChangeType.ADDED, None, dict2[key]))
            elif key not in dict2:
                self.differences.append(Difference(new_path, ChangeType.REMOVED, dict1[key], None))
            else:
                self._deep_compare(dict1[key], dict2[key], new_path)
    
    def _compare_lists(self, list1: List, list2: List, path: str):
        """Compare two lists."""
        if self.ignore_order:
            self._compare_lists_ignore_order(list1, list2, path)
        else:
            self._compare_lists_preserve_order(list1, list2, path)
    
    def _compare_lists_preserve_order(self, list1: List, list2: List, path: str):
        """Compare lists preserving order."""
        max_len = max(len(list1), len(list2))
        
        for i in range(max_len):
            new_path = f"{path}[{i}]"
            
            if i >= len(list1):
                self.differences.append(Difference(new_path, ChangeType.ADDED, None, list2[i]))
            elif i >= len(list2):
                self.differences.append(Difference(new_path, ChangeType.REMOVED, list1[i], None))
            else:
                self._deep_compare(list1[i], list2[i], new_path)
    
    def _compare_lists_ignore_order(self, list1: List, list2: List, path: str):
        """Compare lists ignoring order."""
        # Create copies to avoid modifying original lists
        remaining_list1 = list1.copy()
        remaining_list2 = list2.copy()
        
        # Find matching items
        for i, item1 in enumerate(list1):
            for j, item2 in enumerate(list2):
                if j >= len(remaining_list2):
                    continue
                
                # Create a temporary comparator to check if items are equal
                temp_comparator = JSONComparator(self.ignore_order, self.ignore_case)
                temp_diffs = temp_comparator.compare(item1, item2)
                
                if not temp_diffs:  # Items are equal
                    remaining_list1.remove(item1)
                    remaining_list2.remove(item2)
                    break
        
        # Add remaining items as differences
        for i, item in enumerate(remaining_list1):
            self.differences.append(Difference(f"{path}[removed_{i}]", ChangeType.REMOVED, item, None))
        
        for i, item in enumerate(remaining_list2):
            self.differences.append(Difference(f"{path}[added_{i}]", ChangeType.ADDED, None, item))
    
    def _compare_primitives(self, val1: Any, val2: Any, path: str):
        """Compare primitive values (str, int, float, bool)."""
        if isinstance(val1, str) and isinstance(val2, str) and self.ignore_case:
            if val1.lower() != val2.lower():
                self.differences.append(Difference(path, ChangeType.MODIFIED, val1, val2))
        else:
            if val1 != val2:
                self.differences.append(Difference(path, ChangeType.MODIFIED, val1, val2))


def compare_json_objects(obj1: Any, obj2: Any, ignore_order: bool = False, 
                        ignore_case: bool = False) -> Dict[str, Any]:
    """
    Convenience function to compare two JSON objects.
    
    Args:
        obj1: First JSON object
        obj2: Second JSON object
        ignore_order: If True, ignore order of items in lists
        ignore_case: If True, ignore case when comparing strings
        
    Returns:
        Dictionary containing comparison results
    """
    comparator = JSONComparator(ignore_order, ignore_case)
    differences = comparator.compare(obj1, obj2)
    
    return {
        "total_differences": len(differences),
        "are_equal": len(differences) == 0,
        "differences": [diff.to_dict() for diff in differences],
        "summary": {
            "added": len([d for d in differences if d.change_type == ChangeType.ADDED]),
            "removed": len([d for d in differences if d.change_type == ChangeType.REMOVED]),
            "modified": len([d for d in differences if d.change_type == ChangeType.MODIFIED]),
            "type_changed": len([d for d in differences if d.change_type == ChangeType.TYPE_CHANGED])
        }
    }