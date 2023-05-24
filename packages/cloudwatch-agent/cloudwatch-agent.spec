%global goproject github.com/aws
%global gorepo amazon-cloudwatch-agent
%global goimport %{goproject}/%{gorepo}

%global gover 1.247359.1
%global rpmver %{gover}

%global _dwz_low_mem_die_limit 0

Name: %{_cross_os}cloudwatch-agent
Version: %{rpmver}
Release: 1%{?dist}
Summary: This package provides daemon of Amazon CloudWatch Agent
License: MIT License. Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
URL: https://github.com/aws/amazon-cloudwatch-agent
Source0: https://%{goimport}/archive/v%{gover}/%{gorepo}-%{gover}.tar.gz
#Source1: amazon-cloudwatch-agent-%{gover}.tar.gz

Source1000: clarify.toml

BuildRequires: git
BuildRequires: %{_cross_os}glibc-devel

%description
%{summary}.

%prep
%setup -n %{gorepo}-%{gover} -q

%build
%set_cross_go_flags
go build  -buildmode=pie -ldflags="${GOLDFLAGS}" -o=config-downloader cmd/config-downloader/
go build -buildmode=pie -ldflags="${GOLDFLAGS}" -o=config-translator cmd/config-translator
go build -buildmode=pie -ldflags="${GOLDFLAGS}" -o=amazon-cloudwatch-agent cmd/amazon-cloudwatch-agent
go build -buildmode=pie -ldflags="${GOLDFLAGS}" -o=start-amazon-cloudwatch-agent cmd/start-amazon-cloudwatch-agent

%install

install -d %{buildroot}%{_cross_bindir}
install -p -m 0755 packaging/dependencies/amazon-cloudwatch-agent-ctl %{buildroot}%{_cross_bindir}/amazon-cloudwatch-agent-ctl

%cross_scan_attribution --clarify %{S:1000} go-vendor vendor

%files
%license LICENSE
%{_cross_attribution_file}
%{_cross_attribution_vendor_dir}

