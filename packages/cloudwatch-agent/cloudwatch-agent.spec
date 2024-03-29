%global goproject github.com/aws
%global gorepo amazon-cloudwatch-agent
%global goimport %{goproject}/%{gorepo}

%global gover 1.300034.0
%global rpmver %{gover}

%global _dwz_low_mem_die_limit 0

Name: %{_cross_os}cloudwatch-agent
Version: %{rpmver}
Release: 1%{?dist}
Summary: Amazon Cloudwatch Agent daemon
License: MIT
URL: https://github.com/aws/amazon-cloudwatch-agent
Source0: https://%{goimport}/archive/v%{gover}/%{gorepo}-%{gover}.tar.gz
Source1: bundled-amazon-cloudwatch-agent-%{gover}.tar.gz
Source2: amazon-cloudwatch-agent.json
Source3: cloudwatch-agent-tmpfiles.conf
Source4: amazon-cloudwatch-agent.service
Source5: common-config.toml
Source6: CWAGENT_VERSION

Source1000: clarify.toml

Patch0001: 0001-change-binary-path-to-usr-bin.patch

BuildRequires: %{_cross_os}glibc-devel

%description
%{summary}.

%prep
%setup -n %{gorepo}-%{gover} -q 
%autopatch -p1
%setup -T -D -n %{gorepo}-%{gover} -b 1 -q 

%build
%set_cross_go_flags
go build -buildmode=pie -ldflags="${GOLDFLAGS}" -o=config-translator ./cmd/config-translator
go build -buildmode=pie -ldflags="${GOLDFLAGS}" -o=config-downloader ./cmd/config-downloader
go build -buildmode=pie -ldflags="${GOLDFLAGS}" -o=amazon-cloudwatch-agent ./cmd/amazon-cloudwatch-agent
go build -buildmode=pie -ldflags="${GOLDFLAGS}" -o=start-amazon-cloudwatch-agent ./cmd/start-amazon-cloudwatch-agent

%install
install -d %{buildroot}%{_cross_factorydir}/opt/aws/amazon-cloudwatch-agent/etc
install -p -m 0644 %{S:2} %{buildroot}%{_cross_factorydir}/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
install -p -m 0644 %{S:5} %{buildroot}%{_cross_factorydir}/opt/aws/amazon-cloudwatch-agent/etc/common-config.toml

install -d %{buildroot}%{_cross_bindir}
install -p -m 0755 config-translator %{buildroot}%{_cross_bindir}/config-translator
install -p -m 0755 config-downloader %{buildroot}%{_cross_bindir}/config-downloader
install -p -m 0755 amazon-cloudwatch-agent %{buildroot}%{_cross_bindir}/amazon-cloudwatch-agent
install -p -m 0755 packaging/dependencies/amazon-cloudwatch-agent-ctl %{buildroot}%{_cross_bindir}/amazon-cloudwatch-agent-ctl
install -p -m 0755 start-amazon-cloudwatch-agent  %{buildroot}%{_cross_bindir}/start-amazon-cloudwatch-agent
install -p -m 0644 %{S:6} %{buildroot}%{_cross_bindir}

install -d %{buildroot}%{_cross_tmpfilesdir}
install -p -m 0644 %{S:3} %{buildroot}%{_cross_tmpfilesdir}/cloudwatch-agent-tmpfiles.conf

install -d %{buildroot}%{_cross_unitdir}
install -p -m 0644 %{S:4} %{buildroot}%{_cross_unitdir}

%cross_scan_attribution --clarify %{S:1000} go-vendor vendor

%files
%license LICENSE
%{_cross_attribution_file}
%{_cross_attribution_vendor_dir}
%{_cross_bindir}/amazon-cloudwatch-agent
%{_cross_bindir}/config-translator
%{_cross_bindir}/config-downloader
%{_cross_bindir}/amazon-cloudwatch-agent-ctl
%{_cross_bindir}/start-amazon-cloudwatch-agent
%{_cross_bindir}/CWAGENT_VERSION
%{_cross_factorydir}/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
%{_cross_factorydir}/opt/aws/amazon-cloudwatch-agent/etc/common-config.toml
%{_cross_tmpfilesdir}/cloudwatch-agent-tmpfiles.conf
%{_cross_unitdir}/amazon-cloudwatch-agent.service
