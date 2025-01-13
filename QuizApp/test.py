

class CompanyNote(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="notes")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    before = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    pinned = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company.name} - {self.user.username} - {self.created}"
    
 
 
    
class CompanyNoteSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CompanyNote
        fields = "__all__"   


        
        
@is_login_with_usage()
@api_view(["POST"])
def add_company_note(request, slug):
    try:
        company = Company.objects.get(slug=slug)
    except Company.DoesNotExist:
        return Response({"error": "Company doesnt exist", "error_code": 200}, status=404)

    institution_id = request.COOKIES.get("institution_id")
    institution = Institution.objects.get(id=institution_id)

    note_data = request.data.get("newNote")
    user = request.user

    note_instance = CompanyNote.objects.create(company=company, institution=institution, user=user, note=note_data)
    serializer = CompanyNoteSerializer(note_instance)

    return Response(serializer.data, status=201)


@is_login_with_usage()
@api_view(["PUT"])
def hide_company_note(request, slug, note_id):
    try:
        company = Company.objects.get(slug=slug)
    except Company.DoesNotExist:
        return Response({"error": "Company doesnt exist", "error_code": 200}, status=404)

    try:
        note = CompanyNote.objects.get(id=note_id, company=company)
    except CompanyNote.DoesNotExist:
        return Response(
            {"error": "Note doesn't exist or is not associated with the company", "error_code": 404}, status=404
        )

    note.hidden = True
    note.save()

    return Response({"message": "Note hidden successfully"}, status=200)


@is_login_with_usage()
@api_view(["PUT"])
def edit_company_note(request, slug, note_id):
    try:
        company = Company.objects.get(slug=slug)
    except Company.DoesNotExist:
        return Response({"error": "Company doesnt exist", "error_code": 200}, status=404)

    try:
        note = CompanyNote.objects.get(id=note_id, company=company)
    except CompanyNote.DoesNotExist:
        return Response(
            {"error": "Note doesn't exist or is not associated with the company", "error_code": 404}, status=404
        )

    note.note = request.data.get("editedNote")
    note.created = timezone.now()
    note.save()

    return Response({"message": "Note edited successfully"}, status=200)

    