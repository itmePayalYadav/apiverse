from django.db import models
from core.models import BaseModel  
from core.constants import PRIORITY_CHOICES, PRIORITY_MEDIUM

class Todo(BaseModel):
    title = models.CharField(
        max_length=200,
        help_text="Title of the task",
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional task description",
    )
    completed = models.BooleanField(
        default=False,
        help_text="Whether the task is completed",
    )
    due_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Optional task due date",
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
        help_text="Task priority",
    )

    def __str__(self):
        return f"{self.title} ({self.priority})"

    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todos"
        ordering = ['-created_at'] 
        indexes = [
            models.Index(fields=['due_date']),
            models.Index(fields=['priority']),
            models.Index(fields=['completed']),
        ]

    def soft_delete(self):
        """Soft delete instead of removing the record"""
        self.deleted_at = timezone.now()
        self.save()

    @property
    def status(self):
        """Virtual field to return human-readable status"""
        return "Completed" if self.is_completed else "Pending"

    def __str__(self):
        return f"{self.title} ({self.status})"
    