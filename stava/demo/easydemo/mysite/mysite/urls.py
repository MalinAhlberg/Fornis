from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     url(r'showtext/([^/]*)/(.*)', 'textview.texts.showtextvar'),
     url(r'onelex/([^/]*)', 'textview.texts.onelex'),
     url(r'lexs/all/(.*)', 'textview.texts.showlexall'),
     url(r'lexs/([^/]*)', 'textview.texts.showlex'),
     url(r'text/([^/]*)/(.*)', 'textview.texts.textvar'),
     url(r'text/(.*)', 'textview.texts.text'),
     url(r'textsmall/(.*)', 'textview.texts.textsmall'),
     url(r'^start', 'textview.texts.startempty'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
