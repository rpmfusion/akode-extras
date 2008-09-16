
%if 0%{?fedora} > 2
%define _with_ffmpeg --with-ffmpeg
%define ffmpeg ffmpeg
%endif

Summary: Extra decoder plugins for akode 
Name:	 akode-extras
Version: 2.0.2
Release: 3%{?dist}

License: GPLv2+%{?_with_ffmpeg:/LGPLv2+ (see description)}
Group: 	 System Environment/Libraries
#URL:	 http://carewolf.com/akode/  
URL:     http://www.kde-apps.org/content/show.php?content=30375
Source0: http://www.kde-apps.org/CONTENT/content-files/30375-akode-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch4: akode-2.0.2-gcc43.patch
Patch10: akode-2.0.2-ffmpeg-int64_c.patch
# for newer ffmpeg's that move headers around
Patch11: akode-2.0.2-ffmpeg.patch

BuildRequires: automake
BuildRequires: libmad-devel
%{?_with_ffmpeg:BuildRequires: %{ffmpeg}-devel >= 0.4.9 }
# Be mindful of these, since kdemultimedia-extras-nonfree needs to be rebuilt when/if anything
# is added/removed -- Rex
Provides: %{name}-mpeg_decoder = %{version}-%{release}
%{?_with_ffmpeg:Provides: %{name}-ffmpeg_decoder = %{version}-%{release} }

Requires: akode >= %{version}

%description
%{summary}, including:
* mpeg: Uses libMAD to decoder all MPEG 1/2 layer I-III audio (GPLv2+).
%{?_with_ffmpeg:* ffmpeg: Experimental decoder using the FFMPEG decoding library,}
%{?_with_ffmpeg:  enables WMA and RealAudio playback (LGPLv2+).}


%prep
%setup -q -n akode-%{version}%{?beta}

%patch4 -p1 -b .gcc43

%patch10 -p1 -b .ffmpeg-int64_c
%patch11 -p1 -b .ffmpeg

#[ ! -f configure ] && \
make -f Makefile.cvs


%build
%configure \
  --disable-static \
  --disable-debug --disable-warnings --disable-dependency-tracking \
  --without-libltdl \
  --without-flac \
  --without-oss \
  --without-jack \
  --without-libsamplerate \
  --without-pulseaudio \
  --without-speex \
  --without-vorbis \
  --with-libmad \
  %{?_with_ffmpeg} %{!?_with_ffmpeg:--without-ffmpeg} \

make %{?_smp_mflags}


%check
# Paranoia check, make sure plugins did build correctly
make -C akode/plugins/mpeg_decoder
%{?_with_ffmpeg:make -C akode/plugins/ffmpeg_decoder }


%install
rm -rf %{buildroot}

make -C akode/plugins/mpeg_decoder   install DESTDIR=%{buildroot}
%{?_with_ffmpeg:make -C akode/plugins/ffmpeg_decoder install DESTDIR=%{buildroot}}

# unpackaged files
rm -f %{buildroot}%{_libdir}/lib*.la


%clean
rm -rf %{buildroot}


%files 
%defattr(-,root,root,-)
%{_libdir}/libakode_mpeg_decoder.*
%{?_with_ffmpeg:%{_libdir}/libakode_ffmpeg_decoder.*}


%changelog
* Thu Sep 04 2008 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-3
- fix build 
- spec cosmetics

* Sun Aug 10 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.0.2-2
- rebuild for RPM Fusion

* Sun Dec 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 2.0.2-1
- akode-2.0.2

* Sat Nov 24 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 2.0.1-4
- rebuilt

* Mon Dec 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.1-3
- respin for new ffmpeg

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.1-2
- respin

* Mon Aug 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0.1-1
- 2.0.1

* Mon Apr 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0-5
- Conflicts: kdemultimedia < 6:3.5.0 (for FC-4, mostly)
- Provides: akode-mpeg_decoder, akode-ffmpeg_decoder

-* Sat Apr 01 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 2.0-0.lvn.4
-- enable ffmpeg again

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Jan 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0-0.lvn.3
- disable ffmpeg, pending pkgconfig fix (bug #747)

* Tue Jan 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 2.0-0.lvn.2
- x86_64: drop --with-ffmpeg, for now, until lib detection is fixed
- add %%check section

* Mon Dec 19 2005 Rex Dieter <rexdieter[AT]users.sf.net> 2.0-0.lvn.1
- 2.0(final)

* Wed Nov 23 2005 Rex Dieter <rexdieter[AT]users.sf.net> 2.0-0.lvn.0.4.rc1
- 2.0rc1 

* Wed Nov 23 2005 Rex Dieter <rexdieter[AT]users.sf.net> 2.0-0.lvn.0.3.svn20051123
- svn20051123 snapshot

* Wed Nov 23 2005 Rex Dieter <rexdieter[AT]users.sf.net. 2.0-0.lvn.0.2.b3
- --without-libltdl

* Tue Nov 22 2005 Rex Dieter <rexdieter[AT]users.sf.net> 2.0-0.lvn.0.1.b3
- akode-2.0b3

