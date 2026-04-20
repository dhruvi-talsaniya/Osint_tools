# Examples for OSINT Tools

This script demonstrates the usage of various OSINT tools including IP lookup, domain lookup, email validation, and batch operations.

from osint_tools import IPTool, DomainTool, EmailValidator

# Example of IP lookup
ip_address = '8.8.8.8'
ip_lookup_result = IPTool.lookup(ip_address)
print(f'IP Lookup Result for {ip_address}: {ip_lookup_result}')

# Example of Domain lookup
domain = 'example.com'
domain_lookup_result = DomainTool.lookup(domain)
print(f'Domain Lookup Result for {domain}: {domain_lookup_result}')

# Example of email validation
email = 'test@example.com'
email_validation_result = EmailValidator.validate(email)
print(f'Email Validation Result for {email}: {email_validation_result}')

# Example of batch operations
batch_emails = ['test1@example.com', 'test2@example.com', 'invalid-email']
validation_results = EmailValidator.validate_batch(batch_emails)
print('Batch Email Validation Results:')
for email, result in validation_results.items():
    print(f'{email}: {result}')