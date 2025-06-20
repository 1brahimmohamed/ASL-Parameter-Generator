data = {
    "asl_parameters": [
        [
            "Magnetic Field Strength",
            "3T"
        ],
        [
            "Manufacturer",
            "Siemens"
        ],
        [
            "Manufacturer's Model Name",
            "TrioTim"
        ],
        [
            "PLD Type",
            "multi-PLD"
        ],
        [
            "PASL Type",
            "FAIR"
        ],
        [
            "ASL Type",
            "PASL"
        ],
        [
            "MR Acquisition Type",
            "3D"
        ],
        [
            "Pulse Sequence Type",
            "GRASE"
        ],
        [
            "Echo Time",
            "11.92ms"
        ],
        [
            "Repetition Time",
            "3500ms"
        ],
        [
            "Flip Angle",
            180
        ],
        [
            "In-plane Resolution",
            "8x4mm^2"
        ],
        [
            "Slice Thickness",
            "6mm"
        ],
        [
            "Inversion Time",
            "300ms (1 repeat), 600ms (1 repeat), 900ms (1 repeat), 1200ms (1 repeat), 1500ms (1 repeat), 1800ms (1 repeat), 2100ms (1 repeat), 2400ms (1 repeat), 2700ms (1 repeat), 3000ms (1 repeat)"
        ],
        [
            "Labeling Slab Thickness",
            "115.5mm"
        ],
        [
            "Bolus Cutoff Flag",
            "with"
        ],
        [
            "Bolus Cutoff Technique",
            "Q2TIPS"
        ],
        [
            "Bolus Cutoff Delay Time",
            "from 700ms to 1600ms"
        ],
        [
            "Background Suppression",
            "with"
        ],
        [
            "Background Suppression Number of Pulses",
            2
        ],
        [
            "Background Suppression Pulse Time",
            "150ms and 200ms"
        ],
        [
            "Total Acquired Pairs",
            10
        ]
    ],
    "basic_report": "ASL was acquired on a 3T Siemens TrioTim scanner using multi-PLD FAIR PASL labeling and a 3D GRASE readout with the following parameters: TE = 11.92ms, TR = 3500ms, flip angle 180 degrees, in-plane resolution 8x4mm^2, 18 slices with 6mm thickness, inversion time 300ms (1 repeat), 600ms (1 repeat), 900ms (1 repeat), 1200ms (1 repeat), 1500ms (1 repeat), 1800ms (1 repeat), 2100ms (1 repeat), 2400ms (1 repeat), 2700ms (1 repeat), 3000ms (1 repeat), labeling slab thickness 115.5mm, with bolus saturation using Q2TIPS pulse applied from 700ms to 1600ms after the labeling, with background suppression with 2 pulses at 150ms and 200ms after the start of labeling. In total, 10 label-control pairs were acquired. There is inconsistency in EchoTime between M0 and ASL scans.",
    "errors": {
        "m0_error": [
            [
                "ERROR: Discrepancy in 'EchoTime' for ASL file 'sub-Sub1_asl.json' and M0 file 'sub-Sub1_m0scan.json': ASL value = 11.92, M0 value = 16.14, difference = 4.22, exceeds error threshold 0.1"
            ]
        ]
    },
    "errors_concise": {},
    "errors_concise_text": "",
    "extended_parameters": [],
    "extended_report": "ASL was acquired on a 3T Siemens TrioTim scanner using multi-PLD FAIR PASL labeling and a 3D GRASE readout with the following parameters: TE = 11.92ms, TR = 3500ms, flip angle 180 degrees, in-plane resolution 8x4mm^2, 18 slices with 6mm thickness, inversion time 300ms (1 repeat), 600ms (1 repeat), 900ms (1 repeat), 1200ms (1 repeat), 1500ms (1 repeat), 1800ms (1 repeat), 2100ms (1 repeat), 2400ms (1 repeat), 2700ms (1 repeat), 3000ms (1 repeat), labeling slab thickness 115.5mm, with bolus saturation using Q2TIPS pulse applied from 700ms to 1600ms after the labeling, with background suppression with 2 pulses at 150ms and 200ms after the start of labeling. In total, 10 label-control pairs were acquired. There is inconsistency in EchoTime between M0 and ASL scans.",
    "inconsistencies": "",
    "m0_concise_error": "EchoTime (M0): Discrepancy between ASL JSON and M0 JSON",
    "m0_concise_warning": "",
    "m0_parameters": [
        [
            "M0 Type",
            "Separate"
        ]
    ],
    "major_errors": {},
    "major_errors_concise": {},
    "major_errors_concise_text": "",
    "major_inconsistencies": "",
    "nifti_slice_number": 18,
    "warning_inconsistencies": "",
    "warnings": {},
    "warnings_concise": {},
    "warnings_concise_text": ""
}
