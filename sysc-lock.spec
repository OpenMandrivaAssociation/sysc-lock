%global debug_package %{nil}

Name:		sysc-lock
Version:	0.1.5
Release:	1
Summary:	Wayland session locker for Niri and sysc-shell
License:	BSD-3-Clause
Group:		Window Manager/Bar
URL:		https://github.com/Nomadcxx/%{name}
Source0:	https://github.com/Nomadcxx/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.xz

BuildRequires:	golang
BuildRequires:	pkgconfig(pam)

%description
A Wayland session locker for sysc-shell, with compositor-enforced locking 
and in-process PAM authentication.

%prep
%autosetup -p1
tar -xf %{S:1}

%build
go build -o %{name} ./cmd/%{name}/

%install
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dm644 contrib/systemd/%{name}-session.service %{buildroot}%{_userunitdir}/%{name}-session.service
sed -i 's|%h/.local/bin/|/usr/bin/|g' %{buildroot}%{_userunitdir}/%{name}-session.service

%post
%systemd_user_post %{name}-session.service

%preun
%systemd_user_preun %{name}-session.service

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_userunitdir}/%{name}-session.service
