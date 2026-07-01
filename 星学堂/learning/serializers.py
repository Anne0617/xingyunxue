from rest_framework import serializers
from .models import *

class StudySerializer(serializers.ModelSerializer):
    class Meta: model = Study; fields = "__all__"; read_only_fields = ["id", "submitted_at"]

class ExamSerializer(serializers.ModelSerializer):
    class Meta: model = Exam; fields = "__all__"; read_only_fields = ["id", "created_at"]

class ExamResultSerializer(serializers.ModelSerializer):
    class Meta: model = ExamResult; fields = "__all__"; read_only_fields = ["id", "submitted_at"]

class BadgeSerializer(serializers.ModelSerializer):
    class Meta: model = Badge; fields = "__all__"

class UserBadgeSerializer(serializers.ModelSerializer):
    badge_name = serializers.CharField(source="badge.name", read_only=True)
    class Meta: model = UserBadge; fields = "__all__"; read_only_fields = ["id", "earned_at"]

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta: model = Employee; fields = "__all__"; read_only_fields = ["id", "created_at"]

class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta: model = TrainingProgram; fields = "__all__"; read_only_fields = ["id", "created_at"]

class CheckpointNodeSerializer(serializers.ModelSerializer):
    node_type_display = serializers.CharField(source="get_node_type_display", read_only=True)
    class Meta: model = CheckpointNode; fields = "__all__"; read_only_fields = ["id", "created_at"]

class EmployeeProgramSerializer(serializers.ModelSerializer):
    class Meta: model = EmployeeProgram; fields = "__all__"

class EmployeeCheckpointSerializer(serializers.ModelSerializer):
    class Meta: model = EmployeeCheckpoint; fields = "__all__"
