from django.db import models


class ContactInquiry(models.Model):
    """Contact form submissions from website visitors"""

    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('service', 'Service Request'),
        ('other', 'Other'),
    ]

    # Contact Information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    # Message
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    message = models.TextField()

    # Status
    submitted_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(
        default=False,
        help_text="Mark as read after reviewing"
    )

    # Admin Notes (internal use)
    admin_notes = models.TextField(
        blank=True,
        help_text="Internal notes (not visible to submitter)"
    )

    class Meta:
        ordering = ['-submitted_date']
        verbose_name_plural = "Contact Inquiries"
        indexes = [
            models.Index(fields=['-submitted_date']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} ({self.submitted_date.strftime('%Y-%m-%d')})"

    def mark_as_read(self):
        """Mark inquiry as read"""
        self.is_read = True
        self.save(update_fields=['is_read'])
