- **Calculate Screening Via DSCF**
  - **Iteration 1**
    - ✅ `01-ki` completed  
    - **Power Spectrum Decomposition**
      - **Convert Orbital Files To XML**
        - ✅ `01-bin2xml_total_density` completed  
        - ✅ `02-bin2xml_occ_spin_0_orb_1_density` completed  
        - ✅ `03-bin2xml_occ_spin_0_orb_2_density` completed  
        - ✅ `04-bin2xml_occ_spin_0_orb_3_density` completed  
        - ✅ `05-bin2xml_occ_spin_0_orb_4_density` completed  
        - ✅ `06-bin2xml_emp_spin_0_orb_5_density` completed  
        - ✅ `07-bin2xml_emp_spin_0_orb_6_density` completed  
      - ✅ `02-extract_coefficients_from_xml` completed  
      - ✅ `03-compute_power_spectrum_orbital_1` completed  
      - ✅ `04-compute_power_spectrum_orbital_2` completed  
      - ✅ `05-compute_power_spectrum_orbital_3` completed  
      - ✅ `06-compute_power_spectrum_orbital_4` completed  
      - ✅ `07-compute_power_spectrum_orbital_5` completed  
      - ✅ `08-compute_power_spectrum_orbital_6` completed  
    - **Orbital 1**
      - ✅ `01-dft_n-1` completed  
    - **Orbital 2**
      - ✅ `01-dft_n-1` completed  
    - **Orbital 3**
      - ✅ `01-dft_n-1` completed  
    - **Orbital 4**
      - ✅ `01-dft_n-1` completed  
    - **Orbital 5**
      - ✅ `01-dft_n+1_dummy` completed  
      - ✅ `02-pz_print` completed  
      - ✅ `03-dft_n+1` completed  
    - **Orbital 6**
      - ✅ `01-dft_n+1_dummy` completed  
      - ✅ `02-pz_print` completed  
      - ✅ `03-dft_n+1` completed  

    **α**
    |    |        1 |        2 |        3 |        4 |        5 |        6 |
    |---:|---------:|---------:|---------:|---------:|---------:|---------:|
    |  0 | 0.6      | 0.6      | 0.6      | 0.6      | 0.6      | 0.6      |
    |  1 | 0.493417 | 0.576716 | 0.560552 | 0.492911 | 0.463213 | 0.578981 |

    **predicted α**
    |    |        1 |        2 |        3 |        4 |        5 |        6 |
    |---:|---------:|---------:|---------:|---------:|---------:|---------:|
    |  0 | 0.491291 | 0.576154 | 0.560565 | 0.491663 | 0.447122 | 0.608699 |

    **ΔE<sub>i</sub> - λ<sub>ii</sub> (eV)**
    |    |        1 |        2 |        3 |        4 |         5 |          6 |
    |---:|---------:|---------:|---------:|---------:|----------:|-----------:|
    |  0 | 0.991671 | 0.190919 | 0.346885 | 0.999876 | -0.223314 | -0.0793481 |