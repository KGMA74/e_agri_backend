from .serializers import (
    EmployeeCreateSerializer,
    CustomUserSerializer, ProfileSerializer, EmployeeSerializer, FarmerSerializer
)
from .models import Profile, Farmer, Employee
from django.conf import settings 
from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, action, permission_classes
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .permissions import IsAdminOrFarmer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .utils import set_auth_cookie

def test(request):
    from django.shortcuts import render
    return render(request, 'accounts/test.html')

class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            if access_token:
                set_auth_cookie(response, 'access', access_token, settings.AUTH_COOKIE_ACCESS_MAX_AGE)
            if refresh_token:
                set_auth_cookie(response, 'refresh', refresh_token, settings.AUTH_COOKIE_REFRESH_MAX_AGE)
        return response
    
#customisation de la class TokenObtainPairView pour que les tokens passes par les cookies et non les headers donc plus securise
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            if access_token:
                set_auth_cookie(response, 'access', access_token, settings.AUTH_COOKIE_ACCESS_MAX_AGE)
                
            if refresh_token:
                set_auth_cookie(response, 'refresh', refresh_token, settings.AUTH_COOKIE_REFRESH_MAX_AGE)
                
        return response

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs) :
        refresh_token = request.COOKIES.get('refresh')
        
        if refresh_token:
            #si le token refresh dans le la list des cookies
            request.data['refresh'] = refresh_token
            
        response =  super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            access_token = response.data.get('access')
            print("Access token:", access_token)
            
            #on met a jour le access token
            if access_token:
                set_auth_cookie(response, 'access', access_token, settings.AUTH_COOKIE_ACCESS_MAX_AGE)
     
        return response
    

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')
        
        if access_token:
            request = Request(request._request, data={'token': access_token})
            
        return super().post(request, *args, **kwargs)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def LogoutView(request):
    if request.method == 'POST':
        # Supprimer les tokens en mettant leur valeur des cookies à ''
        response = Response(status=status.HTTP_204_NO_CONTENT)
                   
        # Suppressions des cookies
        set_auth_cookie(response, 'access', '', max_age=0)
        set_auth_cookie(response, 'refresh', '', max_age=0)
        
        return response
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class CustomUserViewSet(UserViewSet):
    def handle_user_role(self, user):
        if user.role == "farmer":
            Farmer.objects.create(user=user)
        elif user.role == "employee":
            raise ValidationError("Employee role cannot be created through this endpoint. manage use the endpoint POST /api/employees/")
            # la création d'un employé est gérée dans la vue EmployeeViewSet
            # Operation autorisee uniquement pour les admins ou les agriculteurs
        elif user.role == "admin":
            pass
        else:
            raise ValidationError("Invalid role specified.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():  # Annule tout si une erreur survient
                self.perform_create(serializer)
                user = serializer.instance

                if user.role == "admin" and request.user and not request.user.is_superuser:
                    raise ValidationError("Admin role cannot be created directly.")

                self.handle_user_role(user)
                
        except Exception as e:
            return Response(
                {"detail": f"User registration failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    
   
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsAdminOrFarmer()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeCreateSerializer
        return EmployeeSerializer


    def perform_create(self, serializer):
        user = self.request.user

        if hasattr(user, 'farmer'):
            farmer = user.farmer
            
        elif user.role == 'admin':
            farmer_id = self.request.data.get('farmer_id')

            if not farmer_id:
                raise ValidationError({'farmer_id': 'This field is required for admin users.'})
            try:
                farmer = Farmer.objects.get(pk=farmer_id)
            except Farmer.DoesNotExist:
                raise ValidationError({'farmer_id': 'Invalid farmer ID.'})
        else:
            raise ValidationError("Only farmers or admins can create employees.")

        serializer.save(farmer=farmer)
    

 
# class TeacherViewSet(viewsets.ModelViewSet):
#     queryset = Teacher.objects.all()
#     serializer_class = TeacherSerializer

# class StudentViewSet(viewsets.ModelViewSet):
#     queryset = Student.objects.all()
#     serializer_class = StudentSerializer

#     @action(detail=False, methods=['post'])
#     def request_verification(self, request, pk=None):
#         """Envoyer un code de vérification à l'étudiant pour l'ajouter à un parent."""
#         try:
#             student = Student.objects.get(user__email=request.data.get('email'))
#         except Student.DoesNotExist:
#             return Response(
#                 {'error': 'No student found with this email address'},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         user = request.user
        
#         # Vérifier que l'utilisateur connecté est un parent
#         try:
#             parent = Parent.objects.get(user=user)
#         except Parent.DoesNotExist:
#             return Response(
#                 {'error': 'Only parents can add children to their account'},
#                 status=status.HTTP_403_FORBIDDEN
#             )
        
#         # Créer un code de vérification
#         verification = VerificationCode.objects.create(
#             student=student,
#             parent=parent
#         )
        
#         # Envoyer l'email à l'étudiant
#         student_email = student.user.email
#         if student_email:
#             send_verification_email(student, verification.code, parent)
#             return Response(
#                 {'message': 'Verification code sent to student email'},
#                 status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {'error': 'Student has no email address'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#     @action(detail=True, methods=['post'])
#     def verify_and_add(self, request, pk=None):
#         """Vérifier le code et ajouter l'étudiant comme enfant."""
#         student = self.get_object()
#         user = request.user
#         verification_code = request.data.get('code')
        
#         if not verification_code:
#             return Response(
#                 {'error': 'Verification code is required'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             parent = Parent.objects.get(user=user)
#         except Parent.DoesNotExist:
#             return Response(
#                 {'error': 'Only parents can add children'}, 
#                 status=status.HTTP_403_FORBIDDEN
#             )
        
#         # Vérifier le code
#         try:
#             verification = VerificationCode.objects.get(
#                 student=student,
#                 parent=parent,
#                 code=verification_code,
#                 is_used=False
#             )
            
#             if not verification.is_valid:
#                 return Response(
#                     {'error': 'Verification code has expired'}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
                
#             # Ajouter l'étudiant à la liste des enfants du parent
#             parent.children.add(student)
            
#             # Marquer le code comme utilisé
#             verification.is_used = True
#             verification.save()
            
#             return Response(
#                 {'message': f'Student {student.user.firstname} successfully added as child'},
#                 status=status.HTTP_200_OK
#             )
            
#         except VerificationCode.DoesNotExist:
#             return Response(
#                 {'error': 'Invalid verification code'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#     @action(detail=True, methods=['post'])
#     def enroll(self, request, pk=None):
#         """Inscrire un étudiant à un cours."""
#         student = self.get_object()
#         serializer = EnrollCourseSerializer(data=request.data)
#         if serializer.is_valid():
#             course = get_object_or_404(Course, id=serializer.validated_data['course_id'])
#             student.enroll_in_course(course)
#             return Response({'message': 'Student enrolled successfully'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     @action(detail=True, methods=['get'])
#     def enrolled_courses(self, request, pk=None):
#         """Liste des cours auxquels l'étudiant est inscrit."""
#         student = self.get_object()
#         courses = student.courses_enrolled.all()
#         serializer = CourseSerializer(courses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @action(detail=True, methods=['post'])
#     def drop(self, request, pk=None):
#         """Désinscrire un étudiant d’un cours."""
#         student = self.get_object()
#         serializer = EnrollCourseSerializer(data=request.data)
#         if serializer.is_valid():
#             course = get_object_or_404(Course, id=serializer.validated_data['course_id'])
#             student.courses.remove(course)
#             return Response({'message': 'Student dropped from course'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     @action(detail=True, methods=["post"])
#     def add_xp(self, request, pk=None):
#         """Permet d'ajouter des XP à un élève et de mettre à jour son niveau."""
#         student = self.get_object()
#         points = request.data.get("points")

#         if not points:
#             return Response({"error": "Points are required"}, status=status.HTTP_400_BAD_REQUEST)

#         student.add_xp(points)
#         return Response({"message": f"{points} XP added to {student.user.fullname}. Current level: {student.level.name}"}, status=status.HTTP_200_OK)

# class ParentViewSet(viewsets.ModelViewSet):
#     queryset = Parent.objects.all()
#     serializer_class = ParentSerializer

#     @action(detail=False, methods=['get'])
#     def children(self, request):
#         """Récupère la liste des enfants de l'utilisateur parent connecté."""
#         try:
#             parent = Parent.objects.get(user=request.user)
#         except Parent.DoesNotExist:
#             return Response(
#                 {'error': 'Only parents can access children information'}, 
#                 status=status.HTTP_403_FORBIDDEN
#             )
        
#         children = parent.children.all()
#         serializer = StudentSerializer(children, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     @action(detail=True, methods=['post'])
#     def remove_child(self, request, pk=None):
#         """Supprimer un enfant d’un parent."""
#         parent = self.get_object()
#         serializer = AddChildSerializer(data=request.data)
#         if serializer.is_valid():
#             student = get_object_or_404(Student, id=serializer.validated_data['student_id'])
#             parent.children.remove(student)
#             return Response({'message': 'Child removed successfully'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

# class UserXPViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     @action(detail=True, methods=["get"])
#     def xp(self, request, pk=None):
#         """Retourne l'XP total d'un utilisateur donné."""
#         student = get_object_or_404(Student, pk=pk)
#         return Response({"total_xp": student.xp}, status=status.HTTP_200_OK)

#     @action(detail=True, methods=["get"])
#     def xp_history(self, request, pk=None):
#         """Retourne l'historique des transactions de XP d'un utilisateur."""
#         student = get_object_or_404(Student, pk=pk)
#         transactions = student.xp_transactions.all()
#         serializer = XPTransactionSerializer(transactions, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
# class StudentLevelViewSet(viewsets.ViewSet):
#     queryset = Student.objects.all()

#     @action(detail=True, methods=["get"])
#     def level(self, request, pk=None):
#         """Retourne le niveau actuel de l'élève."""
#         student = self.get_object()
#         return Response({"level": student.level}, status=status.HTTP_200_OK)

