from django import http
from django import forms
from django.dispatch.dispatcher import receiver
from django.views.generic.base import View
from django.shortcuts import get_object_or_404

try:
    from rest_framework.viewsets import GenericViewSet
except ImportError:
    # fallback to view
    GenericViewSet = View

from models import FlowFile, FlowFileChunk
from signals import file_upload_failed


class FlowFileForm(forms.Form):
    file = forms.FileField()



class UploadMixin(object):
    def get_identifier(self, request):
        """ identifier for chunk upload """
        return '%s-%s'.format((request.session.session_key, self.flowIdentifier))[:200]

    def init_upload_mixin(self, request):
        self.get_variables(request)

        # identifier is a combination of session key and flow identifier
        self.identifier = self.get_identifier(request)

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
        self.create_flow_file_db_entry()
        self.handle_chunk(request)
        return self.return_response(self.flow_file.identifier)

    def create_flow_file_db_entry(self, this_identifier=None):

        # use given identifier or temporary
        identifier = self.identifier
        if this_identifier:
            identifier = this_identifier

        # get file or create if doesn't exist the identifier
        self.flow_file, self.flow_file_created = FlowFile.objects.get_or_create(identifier=identifier, defaults={
            'original_filename': self.flowFilename,
            'total_size': self.flowTotalSize,
            'total_chunks': self.flowTotalChunks,
        })

    def handle_chunk(self, request):
        # validate the file form
        form = FlowFileForm(request.POST, request.FILES)
        if not form.is_valid():
            file_upload_failed.send(self.flow_file)
            return self.return_response(form.errors, error=True)

        # avoiding duplicated chucks
        chunk, created = self.flow_file.chunks.get_or_create(number=self.flowChunkNumber, defaults={
            'file': form.cleaned_data['file'],
        })

        if not created and hasattr(form, 'file'):
            chunk.file = form.file
            chunk.size = form.size

        # save chunk every time to update parent
        chunk.save()

    def return_response(self, msg, error=False):
        return http.HttpResponse(msg)


class UploadView(UploadMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.init_upload_mixin(request)
        return super(UploadMixin, self).dispatch(request, *args, **kwargs)

    def get_variables(self, request):
        # get flow variables
        self.flowChunkNumber = int(request.REQUEST.get('flowChunkNumber'))
        self.flowChunkSize = int(request.REQUEST.get('flowChunkSize'))
        self.flowCurrentChunkSize = int(request.REQUEST.get('flowCurrentChunkSize'))
        self.flowTotalSize = int(request.REQUEST.get('flowTotalSize'))
        self.flowIdentifier = request.REQUEST.get('flowIdentifier')
        self.flowFilename = request.REQUEST.get('flowFilename')
        self.flowRelativePath = request.REQUEST.get('flowRelativePath')
        self.flowTotalChunks = int(request.REQUEST.get('flowTotalChunks'))


class UploadViewSet(UploadMixin, GenericViewSet):
    def post(self, request, *args, **kwargs):
        self.init_upload_mixin(request)
        return super(UploadViewSet, self).post(request, *args, **kwargs)

    def get_variables(self, request):
        # get flow variables
        self.flowChunkNumber = int(request.data.get('flowChunkNumber', 0))
        self.flowChunkSize = int(request.data.get('flowChunkSize', 0))
        self.flowCurrentChunkSize = int(request.data.get('flowCurrentChunkSize', 0))
        self.flowTotalSize = int(request.data.get('flowTotalSize', 0))
        self.flowIdentifier = request.data.get('flowIdentifier', None)
        self.flowFilename = request.data.get('flowFilename', None)
        self.flowRelativePath = request.data.get('flowRelativePath', None)
        self.flowTotalChunks = int(request.data.get('flowTotalChunks', 0))


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