from django import http
from django import forms
from django.dispatch.dispatcher import receiver
from django.views.generic.base import View
from django.shortcuts import get_object_or_404

try:
    from rest_framework.views import APIView
except ImportError:
    # fallback to view
    APIView = View

from models import FlowFile, FlowFileChunk
from signals import file_upload_failed


class FlowFileForm(forms.Form):
    file = forms.FileField()



class UploadMixin(object):
    def get_identifier(self, request):
        """ identifier for chunk upload """
        return '%s-%s'.format((request.session.session_key, self.flowIdentifier))[:200]

    def dispatch(self, request, *args, **kwargs):
        self.get_variables(request)

        # identifier is a combination of session key and flow identifier
        self.identifier = self.get_identifier(request)
        return super(UploadMixin, self).dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Flow.js test if chunk exist before upload it again.
        Return 200 if exist.
        """
        get_object_or_404(FlowFileChunk, number=self.flowChunkNumber, parent__identifier=self.identifier)
        return self.return_response(self.identifier)

    def post(self, request, *args, **kwargs):
        """
        Upload the file by chunks
        """

        # get file or create if doesn't exist the identifier
        flow_file, created = FlowFile.objects.get_or_create(identifier=self.identifier, defaults={
            'original_filename': self.flowFilename,
            'total_size': self.flowTotalSize,
            'total_chunks': self.flowTotalChunks,
        })

        # validate the file form
        form = FlowFileForm(request.POST, request.FILES)
        if not form.is_valid():
            file_upload_failed.send(flow_file)
            return self.return_response(form.errors, error=True)

        # avoiding duplicated chucks
        chunk, created = flow_file.chunks.get_or_create(number=self.flowChunkNumber, defaults={
            'file': form.cleaned_data['file'],
        })
        if not created:
            chunk.file = form.file
            chunk.size = form.size
            chunk.save()

        return self.return_response(flow_file.identifier)

    def return_response(self, msg, error=False):
        return http.HttpResponse(msg)


class UploadView(UploadMixin, View):
    def get_variables(self, request):
        # get flow variables
        self.flowChunkNumber = int(request.REQUEST.get('flowChunkNumber'))
        self.flowChunckSize = int(request.REQUEST.get('flowChunkSize'))
        self.flowCurrentChunkSize = int(request.REQUEST.get('flowCurrentChunkSize'))
        self.flowTotalSize = int(request.REQUEST.get('flowTotalSize'))
        self.flowIdentifier = request.REQUEST.get('flowIdentifier')
        self.flowFilename = request.REQUEST.get('flowFilename')
        self.flowRelativePath = request.REQUEST.get('flowRelativePath')
        self.flowTotalChunks = int(request.REQUEST.get('flowTotalChunks'))


class UploadViewSet(UploadMixin, APIView):
    def get_variables(self, request):
        # get flow variables
        self.flowChunkNumber = int(request.data.get('flowChunkNumber'))
        self.flowChunckSize = int(request.data.get('flowChunkSize'))
        self.flowCurrentChunkSize = int(request.data.get('flowCurrentChunkSize'))
        self.flowTotalSize = int(request.data.get('flowTotalSize'))
        self.flowIdentifier = request.data.get('flowIdentifier')
        self.flowFilename = request.data.get('flowFilename')
        self.flowRelativePath = request.data.get('flowRelativePath')
        self.flowTotalChunks = int(request.data.get('flowTotalChunks'))


class CheckStateView(View):
    def get(self, request, *args, **kwargs):
        """
        Return the status of the file uploaded. This is important for big files,
        because user don't need to wait for the file to be ready.
        """
        flow = get_object_or_404(FlowFile, identifier=request.GET.get('identifier', ''))
        return http.HttpResponse(flow.state)


# Use in your views
# @receiver(file_is_ready, sender=FlowFile)
# def flow_file_ready(sender, instance, **kwargs):
#     """ File ready Function
#     """
#     pass
#
#
# @receiver(file_joining_failed, sender=FlowFile)
# def flow_file_joining_failed(sender, instance, **kwargs):
#     """ Chunk joining Failed -> delete whole file
#     """
#     instance.delete()
#
#
# @receiver(file_upload_failed, sender=FlowFile)
# def flow_file_upload_failed(sender, instance, **kwargs):
#     """ Chunk joining Failed -> delete whole file
#     """
#     instance.delete()