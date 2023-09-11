## Permalink Feature Workflow

### Server-Side:
1. Generate a JSON response with object IDs, e.g., `{"gemstones": [1,2,3], "art": [1,2]}`.
2. Send this JSON response along with the rendered objects to the client.

### Client-Side:
1. User selects the "Create Permalink" button.
2. An HTMX (or AJAX) request sends the JSON object back to the server using POST (since it's a data-changing operation).

### Server-Side:
1. Receive the JSON object from the client.
2. Generate a hash of the JSON object using a hashing algorithm like SHA-256.

### Database:
1. Execute a "get or create" operation to check if a permalink with the given hash already exists. If not, create a new record.
2. Generate a short URL based on the hash.
3. Save the short URL and the associated JSON object in the database.

### Server-Side:
1. Return the short URL to the client.

### Client-Side:
1. HTMX updates the "Create Permalink" button or a specific page element to display the short URL that leads to the current page's state.


## Database Schema for Permalink Feature

### Tables:

#### Example Model:

```python
class Permalink(models.Model):
    hash = models.CharField(max_length=32, unique=True)
    short_url = models.CharField(max_length=64)
    
    class Meta:
        indexes = [
            models.Index(fields=['hash',]),
            models.Index(fields=['short_url',]),
        ]
```

#### Permalink Table

| Column Name     | Data Type  | Description                                    |
|-----------------|------------|------------------------------------------------|
| id              | AutoField  | Unique ID for each record                      |
| hash            | CharField  | Hash of the JSON object                        |
| short_url       | CharField  | Short URL that maps to the hash                |
| json_object     | JSONField  | The original JSON object containing object IDs |
| created_at      | DateTime   | Timestamp when the record was created          |
| updated_at      | DateTime   | Timestamp when the record was last updated     |

### Constraints:

1. **Unique Constraint**: The `hash` column should be unique to prevent duplicate URLs.
2. **Indexing**: The `hash` and `short_url` columns should be indexed for fast retrieval.
3. **Timestamps**: `created_at` and `updated_at` could be set to auto-update upon creation and modification.

### Relationships:

- No direct foreign key relationships to other tables. The `json_object` serves as the relational data by containing object IDs that can relate to other tables.


### Gotchas
- Handle the case where the permalink tries to fetch deleted or modified objects. Ensure graceful fallbacks or error messages.
- Utilize HTMX to target only the specific container holding the form submission, to prevent a full page reload and a resubmission message.
- Watch out for race conditions: Ensure that the database operations for creating/checking unique slugs are atomic.
- Be cautious with the length and character set of the custom slugs. Validate for invalid characters or overly long names.
  
### Other Ideas
- Allow users to create a unique display name for their permalink (e.g., "shop"). This can be done via an input field during permalink creation.
- Use HTMX to check dynamically if the custom display name is already taken. If it is, update the user interface to ask for a new name.
- Create a user dashboard page that displays all their created permalinks and offers options to modify or delete them.
- Note that if two users create different custom names (shops) with the same set of objects, it may disrupt the unique hash name generation. Consider appending user identification to the hash or offering user-based namespacing.
- Think about rate-limiting or CAPTCHA mechanisms if the service is public to prevent abuse.
