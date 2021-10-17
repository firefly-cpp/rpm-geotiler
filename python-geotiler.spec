 %bcond_with tests

%global pypi_name geotiler

%global _description %{expand:
GeoTiler is a library to create maps using tiles from a map provider.
The main goal of the library is to enable a programmer to create maps
using tiles downloaded from OpenStreetMap, Stamen or other map provider.
The maps can be used by interactive applications or to create data analysis
graphs.}

Name:           python-%{pypi_name}
Version:        0.14.5
Release:        1%{?dist}
Summary:        GeoTiler is a library to create map using tiles from a map provider

License:        GPLv3
URL:            https://github.com/wrobell/%{pypi_name}
Source0:        %{pypi_source}
Patch0:         0001-Remove-one-dependency.patch

BuildRequires:  python3-devel
BuildRequires:  make

BuildArch:      noarch

%description %_description

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  pyproject-rpm-macros

#For documentation
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-rtd-theme}

%if %{with tests}
BuildRequires:  %{py3_dist pytest}
%endif

# For the patch
BuildRequires:  git-core

%description -n python3-%{pypi_name} %_description

%package doc
Summary:        %{summary}

%description doc
Documentation for %{name}.

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info
rm -fv poetry.lock

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

PYTHONPATH=${PWD} sphinx-build-3 doc/ html
rm -rf docs/_build/html/{.doctrees,.buildinfo} -vf

%install
%pyproject_install
%pyproject_save_files geotiler

%check
%if %{with tests}
%{python3} -m pytest
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license COPYING
%doc README
%{_bindir}/geotiler-fetch
%{_bindir}/geotiler-lint
%{_bindir}/geotiler-route

%files doc
%license COPYING
%doc html

%changelog
* Sun Oct 17 2021 Iztok Fister Jr. <iztokf AT fedoraproject DOT org> - 0.14.5-1
- Initial package
