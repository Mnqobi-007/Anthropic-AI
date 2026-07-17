## Architecture Proof: One-File Storage Swap

### Storage Modes
- **Memory Mode**: `STORAGE_TYPE=memory` - Uses `InMemoryItemRepository`
- **PostgreSQL Mode**: `STORAGE_TYPE=postgres` - Uses `JpaItemRepository`

### Files That Change
When switching storage:
1. **Only configuration changes** - Set `STORAGE_TYPE` environment variable
2. **Service layer** (`ItemService.java`) - **UNCHANGED**
3. **Controller layer** (`ItemController.java`) - **UNCHANGED**
4. **Repository interface** - **UNCHANGED**

This proves the repository pattern successfully decouples storage from business logic.

### Verification
```bash
# Memory mode
STORAGE_TYPE=memory docker-compose up -d
# Create data, restart, data is gone (memory)

# PostgreSQL mode
STORAGE_TYPE=postgres docker-compose up -d  
# Create data, restart, data persists (database)