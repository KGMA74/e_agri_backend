from .models import Task
from .serializers import TaskSerializer
from rest_framework.viewsets import ModelViewSet
from accounts.permissions import IsAdminOrFarmerOrReadOnly
from notifications.models import Notification
# Create your views here.


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrFarmerOrReadOnly]
    
    def perform_create(self, serializer):
        task = serializer.save()
        
        print(task.employees.all(), "[]"*50)
        # Envoi de notifs aux employee concernes
        for employee in task.employees.all():
            Notification.objects.create(
                user=employee.user,
                notification_type='task',
                message=f"""
                    Task a faire avant {task.dueDate}
                    {task.description} 
                """,
            )
            
        