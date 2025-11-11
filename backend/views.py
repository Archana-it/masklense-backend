from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from collections import Counter
from .models import User, FacialAnalysis, WeeklySummary
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    FacialAnalysisSerializer,
    WeeklySummarySerializer
)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class FacialAnalysisCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = FacialAnalysisSerializer(data=request.data)
        if serializer.is_valid():
            # Save the image first
            analysis = serializer.save(user=request.user)
            
            # TODO: Add your ML model analysis here
            # For now, returning a mock analysis result
            mock_result = self._mock_facial_analysis()
            analysis.analysis_result = mock_result
            analysis.save()
            
            return Response(
                FacialAnalysisSerializer(analysis).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _mock_facial_analysis(self):
        """Mock analysis result - replace with actual ML model"""
        return {
            'skin_health': {
                'acne': 'low',
                'dark_circles': 'medium',
                'wrinkles': 'low',
                'hydration': 'good'
            },
            'recommendations': [
                'Use moisturizer daily',
                'Get adequate sleep',
                'Stay hydrated'
            ],
            'overall_score': 7.5
        }


class FacialAnalysisListView(generics.ListAPIView):
    serializer_class = FacialAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FacialAnalysis.objects.filter(user=self.request.user)


class FacialAnalysisDetailView(generics.RetrieveAPIView):
    serializer_class = FacialAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FacialAnalysis.objects.filter(user=self.request.user)


class WeeklySummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get current week
        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        # Get or create weekly summary
        summary, created = WeeklySummary.objects.get_or_create(
            user=request.user,
            week_start=week_start,
            defaults={
                'week_end': week_end,
                'total_analyses': 0,
                'summary_data': {}
            }
        )
        
        # Update summary with latest data
        analyses = FacialAnalysis.objects.filter(
            user=request.user,
            created_at__gte=week_start,
            created_at__lte=week_end
        )
        
        summary.total_analyses = analyses.count()
        summary.summary_data = self._generate_summary(analyses)
        summary.save()
        
        return Response(WeeklySummarySerializer(summary).data)
    
    def _generate_summary(self, analyses):
        """Generate weekly summary from analyses"""
        if not analyses.exists():
            return {'message': 'No analyses this week'}
        
        # Aggregate data from all analyses
        skin_issues = []
        scores = []
        
        for analysis in analyses:
            result = analysis.analysis_result
            if result and 'skin_health' in result:
                skin_issues.extend(result['skin_health'].values())
            if result and 'overall_score' in result:
                scores.append(result['overall_score'])
        
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            'total_scans': analyses.count(),
            'average_score': round(avg_score, 2),
            'most_common_issues': dict(Counter(skin_issues).most_common(3)),
            'trend': 'improving' if avg_score > 7 else 'needs_attention'
        }


class WeeklySummaryListView(generics.ListAPIView):
    serializer_class = WeeklySummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return WeeklySummary.objects.filter(user=self.request.user)
