# TODO: Create HTML Test Views for Backend Endpoints

## Step 1: Create Missing Templates
- [x] Create `backend/templates/library.html` for the library view
- [x] Create `backend/templates/upload.html` for the upload view

## Step 2: Add Test URLs
- [x] Add `/test/` URLs to `backend/backend/urls.py` for test dashboard and individual test pages
- [x] Include paths for: /test/, /test/register/, /test/login/, /test/profile/, /test/documents/, /test/chunks/

## Step 3: Create Test Views
- [x] Add test views in `backend/documents/views.py` (or new file) for each test page
- [x] Views should render templates with forms and JavaScript for API calls

## Step 4: Create Test Templates
- [x] Create `backend/templates/test/dashboard.html` - main test dashboard with links
- [x] Create `backend/templates/test/register.html` - form for user registration API
- [x] Create `backend/templates/test/login.html` - form for user login API
- [x] Create `backend/templates/test/profile.html` - display user profile API
- [x] Create `backend/templates/test/documents.html` - forms for document CRUD APIs
- [x] Create `backend/templates/test/chunks.html` - display chunks API

## Step 5: Implement JavaScript for API Testing
- [x] Add JavaScript in each test template to:
  - Handle form submissions
  - Make AJAX calls to APIs
  - Display responses
  - Store and use JWT tokens for authentication

## Step 6: Test and Verify
- [x] Run the server and test each endpoint via the HTML forms
- [x] Ensure JWT authentication works across pages
- [x] Fix any issues found during testing


edit the prompts and fallback text to me be more human like..