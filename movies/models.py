from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Movie(models.Model):
    """
    Movie model representing film data with comprehensive metadata.
    """
    id = models.BigAutoField(primary_key=True)
    # Basic Information
    title = models.CharField(
        max_length=1000, 
        null=True, 
        blank=True,
        help_text="The title of the movie"
    )
    overview = models.TextField(
        null=True, 
        blank=True,
        help_text="A brief description of the movie plot"
    )
    tagline = models.CharField(
        max_length=1000, 
        null=True, 
        blank=True,
        help_text="The movie's tagline or slogan"
    )
    
    # Financial Information
    budget = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="The movie's budget in USD"
    )
    revenue = models.PositiveBigIntegerField(
        null=True, 
        blank=True,
        help_text="The movie's total revenue in USD"
    )
    
    # Technical Information
    runtime = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Movie runtime in minutes"
    )
    release_date = models.DateField(
        null=True, 
        blank=True,
        help_text="The date the movie was released"
    )
    movie_status = models.CharField(
        max_length=50, 
        null=True, 
        blank=True,
        choices=[
            ('Released', 'Released'),
            ('Post Production', 'Post Production'),
            ('In Production', 'In Production'),
            ('Planned', 'Planned'),
            ('Rumored', 'Rumored'),
            ('Canceled', 'Canceled'),
        ],
        help_text="Current status of the movie"
    )
    
    # Popularity and Ratings
    popularity = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Popularity score"
    )
    vote_average = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Average user rating (0-10)"
    )
    vote_count = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Total number of votes"
    )
    
    # Additional Information
    homepage = models.URLField(
        max_length=1000, 
        null=True, 
        blank=True,
        help_text="Official movie website URL"
    )
    
    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['release_date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(vote_average__gte=0) & models.Q(vote_average__lte=10),
                name='vote_average_range'
            ),
            models.CheckConstraint(
                check=models.Q(budget__gte=0),
                name='budget_positive'
            ),
            models.CheckConstraint(
                check=models.Q(revenue__gte=0),
                name='revenue_positive'
            ),
            models.CheckConstraint(
                check=models.Q(runtime__gte=0),
                name='runtime_positive'
            ),
        ]

    def __str__(self):
        """String representation of the movie."""
        return self.title or "Untitled Movie"

    def __repr__(self):
        """Developer representation of the movie."""
        return f"<Movie: {self.title} ({self.release_date})>"

    @property
    def profit(self):
        """Calculate profit (revenue - budget)."""
        if self.budget and self.revenue:
            return self.revenue - self.budget
        return None

    @property
    def profit_margin(self):
        """Calculate profit margin as percentage."""
        if self.budget and self.revenue and self.budget > 0:
            return ((self.revenue - self.budget) / self.budget) * 100
        return None

    @property
    def runtime_formatted(self):
        """Format runtime as hours and minutes."""
        if not self.runtime:
            return None
        hours = self.runtime // 60
        minutes = self.runtime % 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"

    @property
    def is_released(self):
        """Check if the movie has been released."""
        return self.movie_status == 'Released'

    @property
    def is_successful(self):
        """Check if the movie was financially successful (profit > 0)."""
        return self.profit and self.profit > 0

    def get_absolute_url(self):
        """Get the absolute URL for this movie."""
        from django.urls import reverse
        return reverse('movie_detail', kwargs={'pk': self.pk})

    def clean(self):
        """Custom validation for the model."""
        from django.core.exceptions import ValidationError
        
        # Validate release date is not in the future
        if self.release_date and self.release_date > timezone.now().date():
            if self.movie_status == 'Released':
                raise ValidationError({
                    'release_date': 'A released movie cannot have a future release date.'
                })
        
        # Validate vote average and vote count consistency
        if self.vote_average and not self.vote_count:
            raise ValidationError({
                'vote_count': 'Vote count is required when vote average is provided.'
            })
