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
- [ ] Document folder structure to `architecture.md` once planned

## Environment Setup
- [ ] Docker
- [ ] Python Flask
  - [ ] Basic Folder Structure
  - [ ] Quickstart Documentation
  - [ ] Code Documentation
  - [ ] Testing Documentation
- [ ] Jenkins
  - [ ] Configure Jenkins Server
  - [ ] Configure CI/CD
- [ ] Environment Security
  - [x] Configure Branch security
  - [ ] Remote Vault
    - [ ] Setup Remote vault for secure credential/key storage
    - [ ] Link remote vault to CI/CD pipeline

## Production
- [ ] Configure Domain name
  - [ ] Configure subdomains
    - [ ] Jenkins
    - [ ] Nginx Proxy
- [ ] Configure HTTPS
- [ ] Firewall Configurations

## Security

### Encryption / Cryptography
- [ ] HTTPS (Implementation)
- [ ] Password Complexity 
  - [ ] Hash & Salted Passwords (Coding/Implementation)
  - [ ] Password Policies (Coding/Database Implementation)
- [ ] Proper Session ID (e.g. use hashes rather than 1,2,3)
  
### Bruteforce Related
- [ ] Rate Limiting
  - [ ] [Nginx HTTP rate limiting](http://nginx.org/en/docs/http/ngx_http_limit_req_module.html) (Implementation) 
  - [ ] Account Lockout (Database Implementation `[?]`)
  - [ ] Reverse Proxy (CloudFlare `[?]` / External Implementation)

### Logging:
- [ ] Nginx Web Logs
  - [ ] Error[?]
  - [ ] Access[?]

### Input Validation
`<Map out input locations>`
- [ ] Input Validation for SQLi
- [ ] Input Validation for XSS
- [ ] SQLi prepared statements

### HTTP Headers
- [ ] Secure HTTP Headers `[?]`
    - [ ] Content-Security-Policies
- [ ] [Restrict HTTP Methods](https://techtutorialsx.com/2016/12/24/flask-controlling-http-methods-allowed/)

### Others
- [ ] CSRF Token (Coding)
- [ ] Credential Management (Environment Variable / Private Key Storage)
- [ ] 2FA Authentication (External Implementation)
- [ ] Error Handling (Custom Error Pages)
- [ ] WAF (modsecurity[?])
- [ ] Network Level Firewall (iptables / ufw)
- [ ] Code Flow No overlaps (to be done, after product is done, check if any codes will leave loopholes)