# The Project (draft/work-in-progress)

## Start

The motivation for this project was to find data, ask questions that someone in
the industry of the data would want to know, and then actually analyze the data
in a way where we can answer business questions and make strategic decisions.

I was interested in doing a project at the scope that would be as close to being
in a data analytics position in some industry. There is actually two hard challenges:

- Finding a large data set  
- Finding someone who has expertise in the domain the data is of

You might ask why not start with a domain (finance, agriculture, labour, etc.)
first and then find the appropriate data? That sounds like the sensible thing to
do, but it is actually hard finding data sets that are large (\> 10GBs). Even
when the big players - [government, big tech, and open source][datasets] -
do not have that much in terms of size and if they do it is something that is of
no interest of me.

Another point of contingency, is that since this a project out of my own interest,
then the domain should be something of interest as well too. I would quickly find
that there would be a tug-of-war battle between *size* and *domain*.

I was interested in answering a question to do with some domain related to big
industries in Canada, I started thinking about health care since there seems to
be a lot of changes in the news and I know a few people who did the diploma
version of my program and would end up working at the healthcare provider in my
city. So that was that, I have my experts, but no data...

Low and behold that getting healthcare data that is Canadian and you can analyse
is basically impossible. I thought maybe there would be anonymized data, but no.
On websites, such as [Government of Canada][gov] or
[Canadian Institute for Health Information][cihi],
you can find and download data, but it is clear from the output that it uses
aggregated measures and cohort-level reporting. Furthermore, the data is specific
to the report it is part of, not general purpose. In other words, raw and
patient-level data is in restricted analytical layers. This is done to reduce
disclosure and re-identification risks.

At this point I was about to give up on doing something related to healthcare,
but I ended up stumbling upon [Synthea][syn] which generates *synthetic* patient
population data where each patient comes with its own health records.

## Synthea

### The good, bad, and ugly

Synthea is super cool, handy, and perhaps something maybe a healthcare provider
may develop in house some day in Canada. It can output the files into several
types, but I ultimately chose [FHIR](#fhir-format) because it is standard used
in Canada.

There was a glaring problem with Synthea... it is heavily US-based. However, I
was able to find a linked repository called [Synthea International][synint]
which allows you to change the location by downloading the appropriate files and
overwriting the default US ones.

In `synthea/src/main/resources/` I had to change settings in order to output FHIR
(JSON) files in the `synthea.properties` file. I noticed when scrolling through
it that this is where the CSV files are set that contain information for
geography, providers, costs, etc. that the application uses in patient generation.
Some of the file names end in `_ca` which came from the Canada folder from
Synthea International.

It hit me that I can create my own CSV files that have Canadian information in
them, dump in folder, and then change the value in the properties to use that one
instead. This is a tedious thing to do to find all this information myself so I
used generative AI to make me the following files:

```text
rehab_ca.csv
hospice_ca.csv
dialysis_ca.csv
home_health_agencies_ca.csv
```

Just checked to make sure that they were similar to ones that were already there
and had realistic enough data. Then in the properties files you would just change
the file it uses:

```jsonc
generate.providers.rehab.default_file = providers/rehab_ca.csv  
// was rehab.csv before with US stuff
```

Command to run inside synthea folder to generate data:

```bash
./run_synthea -s 42 -p 15000 "British Columbia"
```

Output: A folder in `synthea/output/` called `fhir` with 17,451 patient files, 1
practitioner file, and 1 organization file all in FHIR format of JSON  type.

#### FHIR format

\!\!\!\[+ *discuss stuff here about FHIR and healthcare format standards
&nbsp;  
\!\!\!\
[+ probably want to make a outline picture of what the structure of the JSON object looks like \+\]

## Business Questions

After creating the data, I wanted to inspect some of the patient files to see what
information we got and turns out we got a lot. Each patient bundle has up to 17
unique fields with some also having nested data. Inspecting the data and coming
up questions actually became a long and lengthy process. At first I became really
distressed because it was too much information and we could have so many diverse
types of questions we can ask on the data, but instead I chose to go with a theme
of questions revolving around healthcare utilization and patient groups.

By picking a subject we can then ask more refined question/problem and then from
there ask sub questions:

#### Business Problem

> **How do chronic disease burden and multi-morbidity affect healthcare utilization,
  and which patient groups exhibit patterns of repeated acure-care use?**

So from this it is easier to come up with sub questions and look back at the data
and see what we can use for this analysis without using all the data and adding
as we see fit.

| Business question | Analytical question | Why the organization cares |
| --- | --- | --- |
| **Who is using the healthcare system most heavily?** | Which patients fall into the top 5–10% by encounters, ED visits, inpatient admissions or utilization days? | Identifies populations requiring disproportionate resources |
| **What drives high utilization?** | How do age, multi-morbidity, specific chronic conditions and social factors differ between high and typical utilizers? | Helps identify characteristics associated with demand |
| **Are patients repeatedly returning to acute care?** | How many patients return to ED/acute care within 7, 30 or 90 days? | Useful for care-transition and follow-up planning |
| **Does multi-morbidity increase utilization?** | Compare patients with 0, 1, 2, 3+ chronic conditions on encounters, ED visits and inpatient use | Supports chronic-disease-management planning |
| **Which conditions create the greatest encounter burden?** | Which diagnoses are associated with the most encounters and acute-care visits? | Helps prioritize programs/resources |
| **Is care fragmented?** | How many organizations/providers does each patient see? Are high utilizers interacting with more providers? | Indicates coordination and continuity issues |
| **What happens before an acute-care event?** | Reconstruct encounters, conditions, labs, medications and procedures before ED/inpatient admission | Identifies potential intervention points |
| **How does utilization vary geographically?** | Compare patient location, provider location and organization utilization | Supports service-location and capacity planning |
| **How are chronic diseases being managed over time?** | Track labs/vitals, medications and encounters for diabetes, hypertension, CKD, etc. | Supports longitudinal quality monitoring |
| **Which patients transition to higher-support services?** | What clinical histories precede home care, hospice or other intensive services? | Supports planning for complex-care populations |

Now we can disclose what entries we are going to use in the patient bundles.

```jsonc
{
  'AllergyIntolerance': 15912, 
  'CarePlan': 59541, // investigate why these are the same...
  'CareTeam': 59541, // investigate why these are the same...
  'Claim': 2026390, // may not use - too Americanised
  'Condition': 696285, // * 
  'Device': 106709, 
  'DiagnosticReport': 1105537, 
  'Encounter': 1084095, // * 
  'ExplanationOfBenefit': 2026390, // may not use - too Americanised 
  'ImagingStudy': 87422, 
  'Immunization': 246178, 
  'MedicationRequest': 942295, // * 
  'Observation': 9736649, // * break this down because nested information 
  'Patient': 17451, // * 
  'Procedure': 2994872, // *
  'SupplyDelivery': 491954
}
// * -> being used in analysis
```

\!\!\!\[+ *discuss stuff here about which fields we took from each one of these fields, consider putting in seperate file with link* \+\]

## Let the Ingestion Begin\! \- logging, timeout, azure code, azure permissions

This is the first test and script file I made. I already had the data and this
was just a matter of putting the files into the bronze layer on Azure Data Lake
Storage Gen2. The first hard part is how we are actually going to connect to Azure
from our computer. While anything Microsoft is not my cup of tea, I will give
them this, their documents for their services are actually good.

## Tech Stack \- python, libraries, azure, power bi, quatro MIGHT NOT NEED THIS SEE BELOW, MAIN README WILL HAVE

## Engineer Practices \- TDD, version control, data validation, dev-environment medallion?

### Test-driven development

*maybe right about fakers and mocks too*

> *If you can't write a unit test, don't touch my pipelines*

### Data validation

### Docker development environment

### Logging

### Error handling

## Let the Ingestion Begin\! \- logging, timeout, azure code, azure permissions

## Medallion \-  ETL, bronze, silver, and gold\!

&nbsp;

[datasets]: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/projects/datasets.md
[gov]: https://www.canada.ca/en/services/health/data.html
[cihi]: https://www.cihi.ca/en
[syn]: https://github.com/synthetichealth/synthea
[synint]: https://github.com/synthetichealth/synthea-international/tree/master
