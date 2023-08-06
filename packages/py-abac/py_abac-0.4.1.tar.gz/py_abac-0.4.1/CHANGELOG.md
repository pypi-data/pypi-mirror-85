# v0.1.0 Pre-release

- Basic policy definition. Nested attribute not supported.
- Poor policy lookup performance in storage for large number of policies.

# v0.2.0

- Complete re-factor with better design. Derived from XACML and Vakt
- Powerful support for policy conditions on nested attributes.
- MongoDB policy storage with efficient lookup based on target IDs.
- Supports creation of custom policy storage.
- Supports creation of custom PIP.
- JSON based policy language.

# v0.3.0

- Added Sphinx documentation.
- Code quality checks performed.
- Security checks added.
- Added SQL storage.
- Refactored `Request` class name to `AccessRequest`. The name `Request` still supported for backward compatibility. 

# v0.3.1
- Fixed import dependency error for storage. Updated import statements from `py_abac/storage/__init__.py`. Thanks [dylanmcreynolds](https://github.com/dylanmcreynolds) for PR.

# v0.4.0

- Added `MemoryStorage` backend.
- Added `RedisStorage` backend.
- Added `FileStorage` backend.
- Fixed typos in documentation.
- Removed all import statements from `py_abac/storage/__init__.py`.

# v0.4.1

- Added the `NotEqualsAttribute`, `IsInAttribute`, `IsNotInAttribute`, `AllInAttribute`, `AllNotInAttribute`, `AnyInAttribute` and `AnyNotInAttribute` conditions to policy language.
