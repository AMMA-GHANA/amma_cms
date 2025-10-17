"""Pre-defined templates for common service content blocks"""

BLOCK_TEMPLATES = {
    'outdoor_advertising': {
        'name': 'Outdoor Advertising Permit (Full)',
        'description': 'Complete template for outdoor advertising permit service',
        'blocks': [
            {
                'block_type': 'text',
                'title': '',
                'content': 'Purchase application form(s) from the Accounts Offices of Physical Planning Departments.',
                'order': 0,
            },
            {
                'block_type': 'list',
                'title': 'Basic Requirements',
                'content': 'Application forms duly completed by applicant(s) should be submitted to the Physical Planning Department with the following attachments:',
                'data': {
                    'items': [
                        'Receipt of payment (Application form(s))',
                        "Company's certificate of incorporation/commencement of business",
                        'Business Operating Permit (BOP)',
                        'List of proposed locations and photo montage',
                        'Architectural designs and structural drawings',
                        'Evidence of insurance cover',
                        'Written consent from property owner',
                        'Geotechnical studies/investigation'
                    ]
                },
                'order': 1,
            },
            {
                'block_type': 'steps',
                'title': 'Application Process',
                'content': 'The following step-by-step procedures apply to all outdoor advertisement applications:',
                'data': {
                    'steps': [
                        {
                            'title': 'Submission',
                            'description': 'On submission, an applicant pays a non-refundable application processing fee',
                            'list': [
                                'Corrections to be made (if any)',
                                'Date for site inspection'
                            ]
                        },
                        {
                            'title': 'Processing',
                            'description': 'The Secretariat processes the application within 10 working days',
                            'list': []
                        },
                        {
                            'title': 'Collection',
                            'description': 'Applicant shall pay approved permit fee and annual renewal fees',
                            'list': []
                        }
                    ]
                },
                'order': 2,
            },
            {
                'block_type': 'notice',
                'title': 'Note',
                'content': "All fees (Submission, Approval and Annual Renewal fees) shall be determined based on the Assembly's Fee-Fixing Resolution.",
                'order': 3,
            }
        ]
    },
    'environmental_health': {
        'name': 'Environmental Health Services',
        'description': 'Service grid template for environmental health services',
        'blocks': [
            {
                'block_type': 'text',
                'title': '',
                'content': 'Contemporary environmental health services promoting and protecting public health and safety through collaboration, innovation and strategic standard enforcement.',
                'order': 0,
            },
            {
                'block_type': 'service_grid',
                'title': 'Available Services',
                'content': '',
                'data': {
                    'items': [
                        {
                            'title': 'Food Handlers\' Certificate',
                            'description': 'Food handlers medical screening conducted at sub-municipal laboratories.',
                            'list': ['Process takes two (2) weeks', 'Only medically fit clients receive cards']
                        },
                        {
                            'title': 'Hospitality Premises',
                            'description': 'Comprehensive inspection and monitoring services',
                            'list': ['Standard enforcement', 'Safety inspections', 'Sanitation monitoring', 'Pest control']
                        },
                        {
                            'title': 'Industrial Premises',
                            'description': 'Environmental monitoring and safety compliance',
                            'list': ['Environmental monitoring', 'Pollution control', 'Health and safety standards']
                        }
                    ]
                },
                'order': 1,
            }
        ]
    },
    'waste_management': {
        'name': 'Waste Management Services',
        'description': 'Comprehensive waste management services template',
        'blocks': [
            {
                'block_type': 'text',
                'title': '',
                'content': 'Services range from waste collection and disposal to public cleansing and advisory services. Services are rendered directly or outsourced to private service providers through franchise agreements.',
                'order': 0,
            },
            {
                'block_type': 'service_grid',
                'title': 'Service Categories',
                'content': '',
                'data': {
                    'items': [
                        {
                            'title': 'Solid Waste Collection',
                            'description': 'Mandatory subscription for all property owners and occupiers',
                            'list': ['Register with accredited providers', 'Regular collection services', 'Domestic and commercial properties']
                        },
                        {
                            'title': 'Special Waste Collection',
                            'description': 'Specialized collection services for bulk and hazardous waste',
                            'list': ['Bulk waste evacuation', 'Construction debris', 'E-Waste collection', 'Toxic waste handling']
                        },
                        {
                            'title': 'Cleansing Services',
                            'description': 'Public space maintenance and cleaning',
                            'list': ['Street cleaning', 'Public space maintenance', 'Market cleaning', 'Drain cleaning']
                        }
                    ]
                },
                'order': 1,
            },
            {
                'block_type': 'notice',
                'title': 'Important',
                'content': 'Standard service charges are published annually in the Municipal Fee Fixing Resolution.',
                'order': 2,
            }
        ]
    },
    '3_step_process': {
        'name': '3-Step Process',
        'description': 'Simple 3-step process template',
        'blocks': [
            {
                'block_type': 'steps',
                'title': 'How to Apply',
                'content': '',
                'data': {
                    'steps': [
                        {
                            'title': 'Step 1',
                            'description': 'Submit your application with required documents',
                            'list': []
                        },
                        {
                            'title': 'Step 2',
                            'description': 'Application review and processing',
                            'list': []
                        },
                        {
                            'title': 'Step 3',
                            'description': 'Collect your permit or certificate',
                            'list': []
                        }
                    ]
                },
                'order': 0,
            }
        ]
    },
    'requirements_list': {
        'name': 'Requirements List',
        'description': 'Simple bulleted requirements list',
        'blocks': [
            {
                'block_type': 'list',
                'title': 'Required Documents',
                'content': 'Please submit the following documents with your application:',
                'data': {
                    'items': [
                        'Completed application form',
                        'Valid identification',
                        'Proof of address',
                        'Payment receipt'
                    ]
                },
                'order': 0,
            }
        ]
    },
    'fees_table': {
        'name': 'Fees Table',
        'description': 'Standard fees and charges table',
        'blocks': [
            {
                'block_type': 'table',
                'title': 'Fees and Charges',
                'content': '',
                'data': {
                    'headers': ['Service', 'Fee (GHS)', 'Processing Time'],
                    'rows': [
                        ['Application Fee', '50.00', '1-2 days'],
                        ['Permit Fee', '200.00', '5-7 days'],
                        ['Annual Renewal', '100.00', '3-5 days']
                    ]
                },
                'order': 0,
            }
        ]
    }
}


def get_template(template_key):
    """Get a template by key"""
    return BLOCK_TEMPLATES.get(template_key)


def get_all_templates():
    """Get all available templates"""
    return [
        {
            'key': key,
            'name': template['name'],
            'description': template['description']
        }
        for key, template in BLOCK_TEMPLATES.items()
    ]
