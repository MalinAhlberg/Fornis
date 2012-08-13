from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^starta/', 'textview.test.start'),
     url(r'^textid(\d+)/variantview/(.*)', 'textview.test.viewtextidvariant'),
     url(r'^lemgramview/(.*)', 'textview.test.viewlemgram'),
     url(r'^textid(\d+)', 'textview.test.viewtextid'),
     url(r'.*', 'textview.test.viewtext'),
     #url(r'^lemgramview/(.*)/', 'textview.test.viewlemgram'),
)