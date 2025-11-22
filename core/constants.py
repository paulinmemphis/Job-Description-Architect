"""
Stores static data, templates, and enums for the application.
"""

CAREER_FAMILIES = [
    "Leadership & Management",
    "Administrative Support",
    "General",
    "Program & Project Management",
    "Information Technology",
    "Research & Development",
    "Finance & Accounting",
    "Library & Archives",
]

# --- TEMPLATES ---

DUTIES_TEMPLATES = {
    "Leadership & Management": (
        "Provide strategic leadership and operational oversight for the assigned unit, program, or portfolio, aligning goals with the University's mission and strategic plan;"
        "Develop, implement, and regularly assess policies, procedures, and workflows to improve service delivery, quality, and operational efficiency;"
        "Supervise, coach, and evaluate professional and support staff, including recruitment, onboarding, performance management, and professional development planning;"
        "Oversee budget development, forecasting, and financial stewardship; monitor expenditures, approve transactions, and ensure compliance with University, state, and sponsor requirements;"
        "Lead or participate in cross-functional committees, task forces, and working groups to advance institutional priorities and resolve complex issues;"
        "Use qualitative and quantitative data to inform decision-making, track key performance indicators, and drive continuous improvement initiatives;"
        "Ensure compliance with applicable laws, regulations, accreditation standards, contracts, and institutional policies;"
        "Represent the unit to internal and external stakeholders, including senior leadership, partners, donors, and regulatory bodies;"
        "Identify, develop, and implement opportunities for innovation, process improvement, and enhanced student, faculty, or staff experience;"
        "Perform related duties as assigned to support the successful operation of the unit and achievement of institutional goals"
    ),
    "Administrative Support": (
        "Provide comprehensive administrative and clerical support to assigned leaders, faculty, staff, or programs, ensuring accurate and timely completion of tasks;"
        "Manage calendars, schedule meetings, coordinate appointments, and arrange travel or logistics as needed;"
        "Prepare, proofread, and format correspondence, reports, presentations, and other documents using standard office software;"
        "Maintain electronic and physical records, files, and databases in accordance with University policies and records retention requirements;"
        "Process routine financial and HR transactions such as purchase requisitions, invoices, travel reimbursements, payroll forms, and timekeeping records;"
        "Serve as a first point of contact for visitors, callers, and email inquiries, providing excellent customer service and routing issues to appropriate personnel;"
        "Coordinate meeting logistics, room reservations, materials, catering, and technology support as required;"
        "Assist with data entry, report generation, and basic analysis to support unit operations and compliance reporting;"
        "Monitor office supplies, equipment, and maintenance needs; initiate orders and service requests as appropriate;"
        "Perform other administrative tasks and special projects as assigned to support the efficient operation of the office"
    ),
    "General": (
        "Plan, organize, and carry out professional assignments that support the operational and strategic needs of the department or unit;"
        "Collect, analyze, and interpret data or information relevant to the area of responsibility, and prepare summaries, reports, and recommendations;"
        "Develop, document, and improve business processes, workflows, and standard operating procedures to enhance service quality and efficiency;"
        "Provide subject-matter expertise and consultative support to colleagues, leadership, and campus partners;"
        "Coordinate projects, initiatives, or events, including timelines, deliverables, and communications with stakeholders;"
        "Ensure work products and services comply with University policies, applicable regulations, and established standards;"
        "Use technology tools and systems (e.g., databases, reporting tools, productivity software) to perform analyses and maintain accurate records;"
        "Communicate effectively with internal and external stakeholders, using appropriate formats and channels;"
        "Contribute to a culture of customer service, collaboration, and continuous improvement within the unit;"
        "Perform related duties as assigned in support of departmental and institutional priorities"
    ),
    "Program & Project Management": (
        "Plan, scope, and organize projects or programs, including defining objectives, deliverables, timelines, and resource needs;"
        "Develop and maintain detailed project plans, schedules, and work breakdown structures; monitor progress and adjust plans as needed;"
        "Coordinate the work of cross-functional teams, partners, and stakeholders to ensure timely completion of tasks and deliverables;"
        "Prepare and manage program or project budgets; track expenditures, reconcile accounts, and ensure compliance with funding and sponsor requirements;"
        "Identify, assess, and mitigate project risks and issues; escalate concerns appropriately and implement corrective actions;"
        "Collect, analyze, and report program or project metrics and outcomes to leadership, sponsors, and other stakeholders;"
        "Develop and maintain documentation, including charters, status reports, meeting minutes, requirements, and technical or operational specifications;"
        "Facilitate stakeholder communication through meetings, presentations, and written updates, ensuring clarity of roles and expectations;"
        "Support grant or contract proposal development, reporting, and close-out activities as applicable;"
        "Perform related duties as assigned to ensure successful execution and sustainability of projects and programs"
    ),
    "Information Technology": (
        "Design, develop, configure, or maintain information systems, applications, databases, or infrastructure components to support University operations;"
        "Collaborate with stakeholders to gather and refine business and technical requirements, translating them into functional and technical specifications;"
        "Implement, test, and deploy new solutions or enhancements, following established change management and quality assurance practices;"
        "Monitor system performance, availability, and security; troubleshoot and resolve incidents, problems, and service requests in a timely manner;"
        "Develop and maintain technical documentation, including architecture diagrams, configuration details, runbooks, and user guides;"
        "Apply cybersecurity best practices, including access control, patch management, data protection, and vulnerability remediation;"
        "Integrate systems and data sources using APIs, middleware, or other integration technologies as appropriate;"
        "Provide technical guidance, training, and support to users and colleagues; participate in on-call or after-hours support as required;"
        "Evaluate emerging technologies, tools, and practices and make recommendations for adoption or improvement;"
        "Perform related duties as assigned to ensure robust, secure, and reliable technology services"
    ),
    "Research & Development": (
        "Design, plan, and conduct research studies, experiments, or field investigations in accordance with project objectives and protocols;"
        "Collect, manage, and analyze quantitative and/or qualitative data using appropriate scientific and statistical methods;"
        "Develop, test, and refine experimental procedures, instrumentation, and analytical techniques;"
        "Prepare research reports, manuscripts, presentations, and other scholarly outputs; contribute to conference submissions and publications;"
        "Assist with the preparation of grant proposals, budgets, and progress reports to funding agencies or sponsors;"
        "Maintain research records, documentation, and data repositories in compliance with institutional, sponsor, and regulatory requirements;"
        "Ensure adherence to ethical standards and safety protocols, including human subjects protections, animal care, and laboratory safety as applicable;"
        "Coordinate work with faculty investigators, students, collaborators, and technical staff to achieve project milestones;"
        "Support training and mentoring of students or junior staff in research methods and laboratory or field techniques;"
        "Perform related research duties as assigned to advance the goals of the project, laboratory, or center"
    ),
    "Finance & Accounting": (
        "Prepare, review, and analyze financial transactions, journal entries, and account reconciliations in accordance with generally accepted accounting principles (GAAP) and University policies;"
        "Develop, monitor, and report on budgets for assigned units, programs, or projects; analyze variances and recommend corrective actions;"
        "Compile and validate financial data for internal and external reports, including management reports, grant reports, and regulatory filings;"
        "Ensure accurate and timely processing of invoices, payments, reimbursements, and other accounts payable/receivable activities;"
        "Review financial transactions for compliance with sponsor terms, contracts, and institutional policies, resolving discrepancies as needed;"
        "Assist with audits, reviews, and financial monitoring by preparing schedules, documentation, and explanations for auditors and reviewers;"
        "Advise departmental staff and leadership on appropriate use of accounts, funding sources, and financial policies;"
        "Participate in process improvement initiatives related to financial systems, workflows, and internal controls;"
        "Maintain financial records and documentation in an organized, auditable manner consistent with retention requirements;"
        "Perform other accounting and financial analysis duties as assigned to support sound fiscal management"
    ),
    "Library & Archives": (
        "Provide research, reference, and instructional support to students, faculty, staff, and external users in person and through virtual channels;"
        "Develop, organize, describe, and maintain collections, including print, digital, and archival materials, following established standards and metadata practices;"
        "Evaluate, select, and recommend resources for acquisition, licensing, or de-accessioning in support of teaching, learning, and research;"
        "Design and deliver information literacy, orientations, and other instructional sessions tailored to courses, programs, or user groups;"
        "Create and maintain finding aids, guides, and online resources to facilitate discovery and access to collections;"
        "Implement and support use of library systems, repositories, and discovery tools, collaborating with technical staff as needed;"
        "Ensure proper preservation, handling, and storage of unique, rare, or fragile materials, and coordinate digitization projects as appropriate;"
        "Engage in outreach, exhibits, and programming to promote library and archival collections and services;"
        "Participate in assessment, planning, and committee work to improve library operations and user experience;"
        "Perform related professional duties as assigned in support of the mission and goals of the library or archives"
    ),
}

COMPLEXITY_TEMPLATES = {
    "Leadership & Management": "High: Work is strategic and operational in scope, requiring independent judgment in setting priorities, interpreting policies, allocating resources, and resolving complex issues that affect multiple units or stakeholder groups.",
    "Administrative Support": "Moderate: Work is detail-oriented and deadline-driven, requiring the ability to manage multiple tasks simultaneously, apply established procedures, and resolve routine issues independently while referring non-routine matters to higher-level staff.",
    "General": "Moderate to High: Work involves analyzing information, solving varied problems, and coordinating activities across functions with limited direct supervision. Assignments often require selecting and adapting methods to meet unit needs.",
    "Program & Project Management": "High: Work involves managing multiple concurrent projects or programs with defined deliverables, deadlines, and budgets, coordinating cross-functional teams, and making decisions in a dynamic environment with competing priorities.",
    "Information Technology": "High: Work requires advanced technical knowledge, problem solving in complex systems environments, and the ability to design and implement solutions that balance security, usability, performance, and maintainability.",
    "Research & Development": "High: Work requires advanced disciplinary knowledge, independent design of research approaches, interpretation of complex data, and adaptation of methods to address novel scientific or technical questions.",
    "Finance & Accounting": "High: Work requires detailed analysis, application of accounting principles, and interpretation of regulatory and sponsor requirements, with significant consequences for financial accuracy, compliance, and institutional risk.",
    "Library & Archives": "Moderate to High: Work requires professional judgment in developing collections, describing and preserving materials, and designing services, often balancing user needs, resource constraints, and evolving technologies.",
}

IMPACT_TEMPLATES = {
    "Leadership & Management": "High: Decisions and leadership directly influence the effectiveness, culture, budget, and performance of the unit and can have significant impact on institutional priorities, student success, and external relationships.",
    "Administrative Support": "Moderate: Quality, accuracy, and timeliness of work have a strong impact on the efficiency of office operations, service quality, and the ability of leaders and staff to meet deadlines and compliance requirements.",
    "General": "Moderate: Work products and recommendations support decision-making, process improvement, and service delivery within the department, influencing operational effectiveness and stakeholder satisfaction.",
    "Program & Project Management": "High: Successful planning and execution of programs and projects affect service delivery, stakeholder satisfaction, compliance with sponsor or regulatory requirements, and achievement of institutional goals.",
    "Information Technology": "High: Systems, applications, and infrastructure managed in this role are critical to teaching, research, and administrative operations; errors or downtime can significantly disrupt institutional activities.",
    "Research & Development": "High: Research outcomes contribute to the University's scholarly reputation, external funding, and innovation, and may inform policy, practice, or commercial applications.",
    "Finance & Accounting": "High: Accuracy and integrity of financial work directly affect budget management, compliance with regulations and sponsor terms, audit results, and the institution's financial position and credibility.",
    "Library & Archives": "Moderate to High: Quality of collections, discovery tools, and user support directly impacts teaching, learning, and research productivity across the institution.",
}

PROGRESSION_TEMPLATES = {
    "Leadership & Management": "Typical progression may include roles such as Coordinator or Specialist; Assistant or Associate Director or Manager; Director; and, depending on unit size and structure, Executive Director, Associate Vice President, or Vice President.",
    "Administrative Support": "Typical progression may include roles such as Administrative Assistant or Office Coordinator; Senior Administrative Assistant or Executive Assistant; Administrative Coordinator or Office Manager; and, in some cases, Business Manager or Professional Staff roles.",
    "General": "Typical progression may include entry-level professional roles; intermediate or senior analyst/specialist positions; and, with experience, lead, manager, or director roles in related functional areas.",
    "Program & Project Management": "Typical progression may include roles such as Program or Project Coordinator; Program or Project Manager; Senior Program or Project Manager; and, with broader scope, Program Director or Director of Project Management.",
    "Information Technology": "Typical progression may include roles such as Analyst or Developer; Senior Analyst, Engineer, or Developer; Architect or Technical Lead; and, with leadership responsibilities, Manager, Director, or Chief Information Officer.",
    "Research & Development": "Typical progression may include roles such as Research Assistant or Technician; Research Associate or Specialist; Senior Research Associate or Scientist; and, with advanced degrees and funding, Principal Investigator, Research Professor, or Center Director.",
    "Finance & Accounting": "Typical progression may include roles such as Accounting Technician or Analyst; Senior Accountant or Senior Analyst; Accounting Manager or Business Manager; and, with broader responsibilities, Director of Finance, Controller, or Chief Financial Officer.",
    "Library & Archives": "Typical progression may include roles such as Library/Archives Assistant; Librarian or Archivist; Senior or Subject Librarian/Archivist; Department Head or Associate Dean; and, with expanded leadership responsibilities, Dean or Director of Libraries or Archives.",
}

# --- FALLBACKS ---

FALLBACK_DUTIES = (
    "Perform professional duties that support the mission, goals, and daily operations of the assigned unit;"
    "Collaborate with colleagues and stakeholders to deliver high-quality services and solutions;"
    "Maintain accurate records and documentation in accordance with University policies;"
    "Use technology and data to inform decisions and improve processes;"
    "Communicate clearly and professionally with internal and external stakeholders;"
    "Ensure compliance with relevant policies, procedures, and regulations;"
    "Contribute to a positive, inclusive, and service-oriented work environment;"
    "Perform other duties as assigned"
)

FALLBACK_COMPLEXITY = "Moderate: Work involves a mix of routine and non-routine tasks, requiring independent judgment in applying established procedures and adapting approaches to meet unit needs."

FALLBACK_IMPACT = "Moderate: Quality and timeliness of work affect the efficiency and effectiveness of departmental operations and the experience of students, faculty, staff, and other stakeholders."

FALLBACK_PROGRESSION = "Career progression may include movement to more senior or specialized roles within the same functional area, as well as opportunities to assume supervisory, managerial, or cross-functional responsibilities."