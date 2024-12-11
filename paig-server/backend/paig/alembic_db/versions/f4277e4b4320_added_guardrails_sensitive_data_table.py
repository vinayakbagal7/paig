"""added guardrails sensitive data table

Revision ID: f4277e4b4320
Revises: 8026d07174b9
Create Date: 2024-12-11 12:09:29.157184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from core.utils import current_utc_time


# revision identifiers, used by Alembic.
revision: str = 'f4277e4b4320'
down_revision: Union[str, None] = '8026d07174b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('gr_sensitive_data',
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('label', sa.String(length=255), nullable=False),
    sa.Column('guardrail_provider', sa.Enum('AWS', 'PAIG', 'LLAMA', 'OPENAI', 'MULTIPLE', name='guardrailprovider'), nullable=False),
    sa.Column('description', sa.String(length=4000), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('create_time', sa.DateTime(), nullable=False),
    sa.Column('update_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gr_sensitive_data_create_time'), 'gr_sensitive_data', ['create_time'], unique=False)
    op.create_index(op.f('ix_gr_sensitive_data_id'), 'gr_sensitive_data', ['id'], unique=False)
    op.create_index(op.f('ix_gr_sensitive_data_update_time'), 'gr_sensitive_data', ['update_time'], unique=False)

    # ### Inserting system defined sensitive data for PAIG ###
    connection = op.get_bind()
    connection.execute(
        sa.text("""
                    INSERT INTO gr_sensitive_data (status, create_time, update_time, guardrail_provider, label, name, description)
                    VALUES 
                        (1, :now, :now, 'PAIG', 'AU_ABN', 'AU_ABN', 'The Australian Business Number (ABN) is a unique 11 digit identifier issued to all entities registered in the Australian Business Register (ABR)'),
                        (1, :now, :now, 'PAIG', 'AU_ACN', 'AU_ACN', 'An Australian Company Number is a unique nine-digit number issued by the Australian Securities and Investments Commission to every company registered under the Commonwealth Corporations Act 2001 as an identifier'),
                        (1, :now, :now, 'PAIG', 'AU_MEDICARE', 'AU_MEDICARE', 'Medicare number is a unique identifier issued by Australian Government that enables the cardholder to receive a rebates of medical expenses under Australia''s Medicare system'),
                        (1, :now, :now, 'PAIG', 'AU_TFN', 'AU_TFN', 'The tax file number (TFN) is a unique identifier issued by the Australian Taxation Office to each taxpaying entity'),
                        (1, :now, :now, 'PAIG', 'CREDIT_CARD', 'CREDIT_CARD', 'A credit card number is between 12 to 19 digits. https://en.wikipedia.org/wiki/Payment_card_number'),
                        (1, :now, :now, 'PAIG', 'CRYPTO', 'CRYPTO', 'A Crypto wallet number. Currently only Bitcoin address is supported'),
                        (1, :now, :now, 'PAIG', 'DATE_TIME', 'DATE_TIME', 'Absolute or relative dates or periods or times smaller than a day'),
                        (1, :now, :now, 'PAIG', 'EMAIL_ADDRESS', 'EMAIL_ADDRESS', 'An email address identifies an email box to which email messages are delivered'),
                        (1, :now, :now, 'PAIG', 'ES_NIF', 'ES_NIF', 'A spanish NIF number (Personal tax ID)'),
                        (1, :now, :now, 'PAIG', 'IBAN_CODE', 'IBAN_CODE', 'The International Bank Account Number (IBAN) is an internationally agreed system of identifying bank accounts across national borders to facilitate the communication and processing of cross border transactions with a reduced risk of transcription errors'),
                        (1, :now, :now, 'PAIG', 'IP_ADDRESS', 'IP_ADDRESS', 'An Internet Protocol (IP) address (either IPv4 or IPv6)'),
                        (1, :now, :now, 'PAIG', 'IT_FISCAL_CODE', 'IT_FISCAL_CODE', 'An Italian personal identification code. https://en.wikipedia.org/wiki/Italian_fiscal_code'),
                        (1, :now, :now, 'PAIG', 'IT_DRIVER_LICENSE', 'IT_DRIVER_LICENSE', 'An Italian driver license number'),
                        (1, :now, :now, 'PAIG', 'IT_VAT_CODE', 'IT_VAT_CODE', 'An Italian VAT code number'),
                        (1, :now, :now, 'PAIG', 'IT_PASSPORT', 'IT_PASSPORT', 'An Italian passport number'),
                        (1, :now, :now, 'PAIG', 'IT_IDENTITY_CARD', 'IT_IDENTITY_CARD', 'An Italian identity card number. https://en.wikipedia.org/wiki/Italian_electronic_identity_card'),
                        (1, :now, :now, 'PAIG', 'LOCATION', 'LOCATION', 'Name of politically or geographically defined location (cities, provinces, countries, international regions, bodies of water, mountains'),
                        (1, :now, :now, 'PAIG', 'MEDICAL_LICENSE', 'MEDICAL_LICENSE', 'Common medical license numbers'),
                        (1, :now, :now, 'PAIG', 'NRP', 'NRP', 'A person’s Nationality, religious or political group'),
                        (1, :now, :now, 'PAIG', 'PERSON', 'PERSON', 'A full person name, which can include first names, middle names or initials, and last names'),
                        (1, :now, :now, 'PAIG', 'PHONE_NUMBER', 'PHONE_NUMBER', 'A telephone number'),
                        (1, :now, :now, 'PAIG', 'SG_NRIC_FIN', 'SG_NRIC_FIN', 'A National Registration Identification Card'),
                        (1, :now, :now, 'PAIG', 'UK_NHS', 'UK_NHS', 'A UK NHS number is 10 digits'),
                        (1, :now, :now, 'PAIG', 'URL', 'URL', 'A URL (Uniform Resource Locator), unique identifier used to locate a resource on the Internet'),
                        (1, :now, :now, 'PAIG', 'US_BANK_NUMBER', 'US_BANK_NUMBER', 'A US bank account number is between 8 to 17 digits'),
                        (1, :now, :now, 'PAIG', 'US_DRIVER_LICENSE', 'US_DRIVER_LICENSE', 'A US driver license according to https://ntsi.com/drivers-license-format/'),
                        (1, :now, :now, 'PAIG', 'US_ITIN', 'US_ITIN', 'US Individual Taxpayer Identification Number (ITIN). Nine digits that start with a "9" and contain a "7" or "8" as the 4 digit'),
                        (1, :now, :now, 'PAIG', 'US_PASSPORT', 'US_PASSPORT', 'A US passport number with 9 digits'),
                        (1, :now, :now, 'PAIG', 'US_SSN', 'US_SSN', 'A US Social Security Number (SSN) with 9 digits')
                """),
        {"now": current_utc_time()}
    )

    # ### Inserting system defined sensitive data for AWS ###
    connection.execute(
        sa.text("""
            INSERT INTO gr_sensitive_data (status, create_time, update_time, guardrail_provider, label, name, description)
            VALUES 
                (1, :now, :now, 'AWS', 'Name', 'NAME', 'Name of the person'),
                (1, :now, :now, 'AWS', 'Phone', 'PHONE', 'Phone number of the person'),
                (1, :now, :now, 'AWS', 'Address', 'ADDRESS', 'Physical or mailing address of the person'),
                (1, :now, :now, 'AWS', 'Age', 'AGE', 'Age of the person'),
                (1, :now, :now, 'AWS', 'Username', 'USERNAME', 'Unique identifier for a user account'),
                (1, :now, :now, 'AWS', 'Password', 'PASSWORD', 'Secure key used to access a system'),
                (1, :now, :now, 'AWS', 'Driver ID', 'DRIVER_ID', 'Driver identification number'),
                (1, :now, :now, 'AWS', 'License Plate', 'LICENSE_PLATE', 'License plate number of the vehicle'),
                (1, :now, :now, 'AWS', 'Vehicle Identification Number', 'VEHICLE_IDENTIFICATION_NUMBER', 'Unique code to identify a motor vehicle'),
                (1, :now, :now, 'AWS', 'CVV', 'CREDIT_DEBIT_CARD_CVV', 'Card Verification Value for credit or debit cards'),
                (1, :now, :now, 'AWS', 'Credit/Debit Card Expiry', 'CREDIT_DEBIT_CARD_EXPIRY', 'Expiry date of a credit or debit card'),
                (1, :now, :now, 'AWS', 'Credit/Debit Card Number', 'CREDIT_DEBIT_CARD_NUMBER', 'Unique number of a credit or debit card'),
                (1, :now, :now, 'AWS', 'PIN', 'PIN', 'Personal identification number used for security'),
                (1, :now, :now, 'AWS', 'International Bank Account Number', 'INTERNATIONAL_BANK_ACCOUNT_NUMBER', 'Globally recognized bank account number'),
                (1, :now, :now, 'AWS', 'SWIFT Code', 'SWIFT_CODE', 'Code to identify banks for international transactions'),
                (1, :now, :now, 'AWS', 'IPv4 Address', 'IP_ADDRESS', 'Unique address for devices on a network'),
                (1, :now, :now, 'AWS', 'MAC Address', 'MAC_ADDRESS', 'Unique identifier for a network interface'),
                (1, :now, :now, 'AWS', 'Web Address', 'URL', 'Uniform Resource Locator to identify resources on the internet'),
                (1, :now, :now, 'AWS', 'AWS Access Key', 'AWS_ACCESS_KEY', 'Key used to access AWS resources'),
                (1, :now, :now, 'AWS', 'AWS Secret Key', 'AWS_SECRET_KEY', 'Secret key used for AWS authentication'),
                (1, :now, :now, 'AWS', 'US Passport Number', 'US_PASSPORT_NUMBER', 'Passport number issued in the United States'),
                (1, :now, :now, 'AWS', 'US Social Security Number', 'US_SOCIAL_SECURITY_NUMBER', 'Social Security Number issued in the United States'),
                (1, :now, :now, 'AWS', 'US Individual Taxpayer Identification Number', 'US_INDIVIDUAL_TAX_IDENTIFICATION_NUMBER', 'Taxpayer Identification Number issued in the United States'),
                (1, :now, :now, 'AWS', 'US Bank Account Number', 'US_BANK_ACCOUNT_NUMBER', 'Bank account number in the United States'),
                (1, :now, :now, 'AWS', 'US Bank Routing Number', 'US_BANK_ROUTING_NUMBER', 'Bank routing number in the United States'),
                (1, :now, :now, 'AWS', 'Canadian Health Service Number', 'CA_HEALTH_NUMBER', 'Health Service Number in Canada'),
                (1, :now, :now, 'AWS', 'Canadian Social Insurance Number', 'CA_SOCIAL_INSURANCE_NUMBER', 'Social Insurance Number in Canada'),
                (1, :now, :now, 'AWS', 'UK Unique Taxpayer Reference', 'UK_UNIQUE_TAXPAYER_REFERENCE_NUMBER', 'Unique Taxpayer Reference number in the United Kingdom'),
                (1, :now, :now, 'AWS', 'UK National Insurance Number', 'UK_NATIONAL_INSURANCE_NUMBER', 'National Insurance Number in the United Kingdom'),
                (1, :now, :now, 'AWS', 'UK National Health Service Number', 'UK_NATIONAL_HEALTH_SERVICE_NUMBER', 'National Health Service Number in the United Kingdom')
        """),
        {"now": current_utc_time()}
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_gr_sensitive_data_update_time'), table_name='gr_sensitive_data')
    op.drop_index(op.f('ix_gr_sensitive_data_id'), table_name='gr_sensitive_data')
    op.drop_index(op.f('ix_gr_sensitive_data_create_time'), table_name='gr_sensitive_data')
    op.drop_table('gr_sensitive_data')
    # ### end Alembic commands ###
