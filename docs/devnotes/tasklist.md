# Tasklist
All major and minor objectives for the project's achievement can be added here.

## Legend
- Not sure how/are we implementing -> `[?]`
- Pre-requisite -> `<>`

## Documentation
- [ ] Adding Python Doc comments for flask routes
- [x] Ensure '`$`' in front of linux commands
- [ ] Add Mermaid Diagrams where applicable
- [x] Finish Git GPG setup guide
- [x] Update all command lines to `console` for markdown codeblock format
- [x] Document folder structure to `architecture.md` once planned


## Environment Setup
- [ ] Web App
  - [x] Python Flask
    - [x] Basic Folder Structure
    - [x] Quickstart Documentation
    - [x] Update environment variables to use secrets
  - [x] Postgresql
    - [x] Basic setup
    - [x] Update environment variables to use secrets
  - [x] Gunicorn
    - [x] Basic setup
    - [x] Secure setup
  - [x] Nginx
    - [x] Basic setup
    - [ ] Security
    - [x] Optimze `Dockerfile`
  - [x] Docker
- [x] Jenkins
  - [x] Configure Jenkins Server
- [ ] Environment Security
  - [x] Configure Branch security
  - [ ] Jenkins CI/CD pipeline secret management

## Jenkins
- [x] Configure OWASP Plugin
- [x] Configure General plugins
- [ ] Configure CI testing
- [x] Configure CD once production level is staged
- [x] Configure TLS/SSL for Apache

## Production
- [x] Refine `docker-compose.yml` for production deployment
- [ ] Configure Domain name
  - [ ] Configure subdomains
    - [ ] Jenkins
    - [ ] Nginx Proxy
- [ ] Configure HTTPS
- [x] Firewall Configurations

## Web App
- [ ] Pages
  - [x] Login Page
  - [x] Register
  - [ ] Home dashboard
  - [ ] Patient Records
    - [x] Read Records page
    - [ ] Create/Edit/Delete Records page
  - [ ] Appointments
    - [x] Read Appointments
    - [ ] Create/Edit/Delete Appointments
  - [ ] Clean up templates and other routes
- [x] DB models
  - [x] Implement Linkages between the different models
  - [x] Encryption?
- [ ] SFR
  - [x] Form security
    - [x] Input validation (server-side minimum, client side good to have)
  - [ ] Authentication
    - [ ] Login
    - [ ] Register
      - [ ] Password complexity
      - [ ] 
    - [x] 2FA
     - [x] Email Verification
     - [x] Login OTP
     - [x] Password Reset 2FA
    - [ ] Prevent password brute forcing
  - [ ] RBAC
    - [ ] Each user should have unique tag in session to identify web traffic
    - [ ] Error pages should be shown when user has no authority to access pages
    - [ ] Patient Records
      - [ ] Doctor
        - [ ] Create Record
        - [ ] Edit Record
        - [ ] View Record
      - [ ] Patient
        - [ ] Read own record (Cannot read other records)
        - [ ] 
      - [ ] Nurse
        - [ ] View Record
    - [ ] Appointments
        - [ ] Doctor
          - [ ] Create Record
          - [ ] Edit Record
        - [ ] Patient
          - [ ] Create own appointment (Cannot create for other patients)
        - [ ] Nurse
          - [ ] Create new appointment
- [ ] FSR
  - [ ] Message Integrity (idk how u want to implement this)
  - [ ] Backups (This one also idk how)
  - [ ] Logging
  - [ ] Error management (As little info leaked about server as possible when errors prompted)

### Database
- [x] Learn SQLAlchemy
- [x] Create models
  - [x] Users
  - [x] Appointments
  - [x] Records

## Configuration
- [x] CMS app (flask, gunicorn)
  - [ ] Logging
- [x] Nginx Proxy
  - [x] HTTPS configuration
  - [ ] Logging
- [x] Jenkins Pipeline
  - [x] Secure Secrets configuration

## Testing
- [ ] Static Tests
  - [ ] Test login functions
  - [ ] Test Register functions
  - [ ] 
- [ ] Dynamic Tests
  - [ ] Injections
  - [ ] XSS
  - [ ] CSRF
  - [ ] XSRF
  - [ ] Session Hijacking
  - [ ] LFI
  - [ ] Directory Traversal
  - [ ] Password Bruteforce
  - [ ] Credential Stuffing
  - [ ] Session Fixation
  - [ ] Injection
  - [ ] Source Code Review (Double check the comments)

## General
- [ ] Code Documentation

## Security

### Encryption / Cryptography
- [x] HTTPS (Implementation)
- [x] Password Complexity 
  - [x] Hash & Salted Passwords (Coding/Implementation)
  - [x] Password Policies (Coding/Database Implementation)
- [x] Proper Session ID (e.g. use hashes rather than 1,2,3)
  
### Bruteforce Related
- [x] Rate Limiting
  - [x] [Nginx HTTP rate limiting](http://nginx.org/en/docs/http/ngx_http_limit_req_module.html) (Implementation) 
  - [ ] Account Lockout (Database Implementation `[?]`)
  - [ ] Reverse Proxy (CloudFlare `[?]` / External Implementation)

### Logging:
- [x] Nginx Web Logs
  - [x] Error[?]
  - [x] Access[?]

### Input Validation
`<Map out input locations>`
- [ ] Input Validation for SQLi
- [ ] Input Validation for XSS
- [ ] SQLi prepared statements

### HTTP Headers
- [x] Secure HTTP Headers `[?]`
  - [x] Content-Security-Policies

### Others
- [x] CSRF Token (Coding)
- [x] Credential Management (Environment Variable / Private Key Storage)
- [x] 2FA Authentication (External Implementation)
- [ ] Error Handling (Custom Error Pages)
- [x] Network Level Firewall (iptables / ufw)
- [ ] Code Flow (code review) No overlaps (to be done, after product is done, check if any codes will leave loopholes)