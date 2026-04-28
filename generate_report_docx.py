from datetime import date, datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


OUTPUT_FILE = "Computer_Animation_Project_Report.docx"

UNIVERSITY_NAME = "[University Name]"
FACULTY_NAME = "[Faculty / Department]"
COURSE_NAME = "Computer Animation"
COURSE_CODE = "[Course Code]"
INSTRUCTOR_NAME = "[Instructor Name]"
SEMESTER_INFO = "[Semester / Academic Year]"
AUTHOR_1 = "[Your Name] ([Student ID])"
AUTHOR_2 = "[Teammate Name] ([Student ID])"


def paragraph_xml(text="", style=None, align=None, page_break_before=False, page_break_after=False):
    props = []
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        props.append(f'<w:jc w:val="{align}"/>')
    if page_break_before:
        props.append("<w:pageBreakBefore/>")

    ppr = f"<w:pPr>{''.join(props)}</w:pPr>" if props else ""

    runs = []
    if text:
        safe_text = escape(text)
        runs.append(f"<w:r><w:t xml:space=\"preserve\">{safe_text}</w:t></w:r>")
    if page_break_after:
        runs.append("<w:r><w:br w:type=\"page\"/></w:r>")

    return f"<w:p>{ppr}{''.join(runs)}</w:p>"


def bullet_xml(text):
    safe_text = escape(text)
    return (
        "<w:p>"
        "<w:pPr>"
        "<w:pStyle w:val=\"ListParagraph\"/>"
        "<w:numPr><w:ilvl w:val=\"0\"/><w:numId w:val=\"1\"/></w:numPr>"
        "</w:pPr>"
        f"<w:r><w:t xml:space=\"preserve\">{safe_text}</w:t></w:r>"
        "</w:p>"
    )


def build_document_body():
    today = date.today().strftime("%B %d, %Y")

    body = [
        paragraph_xml(UNIVERSITY_NAME, style="Title", align="center"),
        paragraph_xml(FACULTY_NAME, style="Subtitle", align="center"),
        paragraph_xml("", page_break_before=False),
        paragraph_xml("Real-Time Exercise Tracking System", style="CoverTitle", align="center"),
        paragraph_xml(
            "An Application of Computer Vision and Computer Animation",
            style="CoverSubtitle",
            align="center",
        ),
        paragraph_xml("Formal Project Report", style="Subtitle", align="center"),
        paragraph_xml(f"Course: {COURSE_NAME}", style="Subtitle", align="center"),
        paragraph_xml("", style="Normal"),
        paragraph_xml("Prepared by", style="Heading2", align="center"),
        paragraph_xml(AUTHOR_1, style="Normal", align="center"),
        paragraph_xml(AUTHOR_2, style="Normal", align="center"),
        paragraph_xml("", style="Normal"),
        paragraph_xml(f"Course Code: {COURSE_CODE}", style="Normal", align="center"),
        paragraph_xml(f"Instructor: {INSTRUCTOR_NAME}", style="Normal", align="center"),
        paragraph_xml(f"Semester: {SEMESTER_INFO}", style="Normal", align="center"),
        paragraph_xml(f"Submission Date: {today}", style="Normal", align="center"),
        paragraph_xml(
            "This report documents the design and implementation of a real-time exercise tracking system "
            "that combines pose estimation, motion analysis, and animation-oriented movement interpretation.",
            style="Quote",
            align="center",
            page_break_after=True,
        ),
        paragraph_xml("Preface", style="Heading1"),
        paragraph_xml(
            "This report presents a two-member course project developed for Computer Animation. The project "
            "explores how movement analysis can be studied through the combined use of computer vision and "
            "computer animation. Although the system relies on computer vision to observe the user through a "
            "webcam, the conceptual focus of this report is intentionally placed on computer animation. The "
            "project interprets human exercise as a sequence of poses, transitions, and motion progressions "
            "rather than as isolated image frames."
        ),
        paragraph_xml(
            "The central idea is that each exercise can be described by a start pose, an end pose, and a "
            "continuous transition between them. This is directly aligned with animation practice, in which "
            "key poses define major movement states and interpolation estimates the in-between motion. "
            "MediaPipe landmarks act as a simplified skeleton, allowing the system to observe body joints in "
            "a manner related to motion capture and skeletal animation."
        ),
        paragraph_xml(
            "The following sections provide the project background, theoretical foundations, implementation "
            "summary, exercise descriptions, and conclusions. The discussion highlights how animation "
            "principles such as interpolation, key poses, state transitions, motion continuity, and skeletal "
            "representation are concretely applied in the project."
        ),
        paragraph_xml("Acknowledgements", style="Heading1", page_break_before=True),
        paragraph_xml(
            "We would like to express our sincere gratitude to the course instructor for guidance, academic "
            "support, and constructive feedback throughout the development of this project. We also appreciate "
            "the opportunity provided by the Computer Animation course to study motion not only as a visual "
            "phenomenon but also as a computable structure that can be interpreted, measured, and communicated "
            "through interactive systems."
        ),
        paragraph_xml(
            "This project was completed collaboratively by two students. The work reflects shared effort in "
            "conceptual design, implementation, testing, and report preparation."
        ),
        paragraph_xml("Abstract", style="Heading1", page_break_before=True),
        paragraph_xml(
            "This project presents a real-time exercise tracking system developed as a course project for "
            "Computer Animation. The system combines computer vision and computer animation in order to capture, "
            "interpret, and evaluate human exercise movements from live webcam input. MediaPipe Pose is used to "
            "estimate body landmarks, while OpenCV supports real-time frame processing and visual feedback. "
            "Exercise-specific logic is implemented to detect movement stages, evaluate pose quality, and count "
            "completed repetitions."
        ),
        paragraph_xml(
            "The main academic contribution of the project lies in its animation-oriented interpretation of "
            "motion. Each exercise is modeled through a start pose, an end pose, and a continuous transition "
            "between them. This reflects core animation concepts such as skeletal representation, key poses, "
            "interpolation, temporal continuity, and motion capture. Rather than viewing the system only as a "
            "recognition task, the project treats body motion as articulated movement progressing through a "
            "sequence of meaningful states."
        ),
        paragraph_xml(
            "The final system supports six exercises: Bicep Curl, Shoulder Press, Dumbbell Side Lateral Raise, "
            "Squat, Plank, and High Knees. The project demonstrates that computer animation principles can be "
            "applied effectively beyond traditional content creation and can play an important role in the "
            "analysis of human movement in interactive applications."
        ),
        paragraph_xml("Table of Contents", style="Heading1", page_break_before=True),
    ]

    toc_items = [
        "Preface",
        "Acknowledgements",
        "Abstract",
        "1. Introduction",
        "2. Project Objectives",
        "3. System Overview",
        "4. Theoretical Foundation in Computer Animation",
        "5. Supporting Concepts from Computer Vision",
        "6. Exercise Set and Basic Instructions",
        "7. Implementation Summary",
        "8. Results and Discussion",
        "9. Conclusion",
        "10. Future Improvements",
        "References",
    ]
    body.extend(bullet_xml(item) for item in toc_items)

    sections = [
        ("1. Introduction", [
            "The project is a real-time exercise tracking system implemented with Python, OpenCV, MediaPipe, "
            "and a web-based interface. The system receives video from a webcam, estimates body landmarks, "
            "computes joint relationships, and uses those measurements to evaluate exercise execution. It can "
            "switch between multiple exercise types and display live feedback such as repetition count, motion "
            "stage, and progress percentage.",
            "From an animation perspective, the system is not merely recognizing a person in front of a camera. "
            "Instead, it is interpreting human motion as a structured sequence of poses linked by continuous "
            "transitions over time. This makes the project especially relevant to Computer Animation because it "
            "transforms observed movement into skeletal data, pose states, and interpolated motion progress.",
        ]),
        ("2. Project Objectives", [
            ("bullet", "To design a real-time exercise tracking application that automatically analyzes body motion and provides understandable visual feedback."),
            ("bullet", "To demonstrate how computer animation principles such as skeletal representation, key poses, and interpolation can be applied to motion analysis."),
            ("bullet", "To integrate computer vision techniques for body landmark detection with animation-oriented reasoning about movement."),
            ("bullet", "To support multiple exercises and explain each movement through meaningful motion stages."),
        ]),
        ("3. System Overview", [
            "The system consists of three main layers. The first layer is video acquisition and pose estimation, "
            "where webcam frames are processed and body landmarks are extracted. The second layer is "
            "exercise-specific motion analysis, where each exercise class interprets the landmark configuration "
            "according to its own movement rules. The third layer is user feedback, where the current exercise "
            "name, repetition count, stage, and motion percentage are displayed on the live video stream and the "
            "web dashboard.",
            "This layered structure supports a modular interpretation of movement. Each exercise is modeled as a "
            "specific animation-like motion pattern with a clear beginning, progression, and completion. Because "
            "the exercise logic is encapsulated in separate modules, the project can be extended with new "
            "movements without redesigning the entire pipeline.",
        ]),
        ("4. Theoretical Foundation in Computer Animation", [
            ("subheading", "4.1 Skeletal Representation and Rig Analogy"),
            "MediaPipe represents the human body through landmarks located at key joints such as shoulders, "
            "elbows, wrists, hips, knees, ankles, and other body points. When these landmarks are connected, they "
            "form a simplified skeleton similar to the rig structure used in computer animation. In a traditional "
            "animation pipeline, a character rig defines how limbs are connected and how movement can be described "
            "through joints. In this project, the body landmarks play a comparable role by providing a structured "
            "articulation model for motion analysis.",
            ("subheading", "4.2 Key Poses and Pose-to-Pose Thinking"),
            "Each exercise can be broken into major poses such as down, up, hold, or adjust. This is closely "
            "related to pose-to-pose animation, where an animator first defines important key poses and then "
            "constructs the in-between movement. For example, a bicep curl has a clear lowered-arm pose and a "
            "flexed-arm pose. A squat has an upright standing pose and a lowered pose at the bottom of the "
            "movement. By detecting when the body reaches these major states, the project applies the same logic "
            "used to organize movement in animation.",
            ("subheading", "4.3 Interpolation Between Start and End Poses"),
            "Interpolation is one of the most important animation concepts in this project. For every supported "
            "exercise, there is a start pose and an end pose. The motion between them does not need to be defined "
            "frame by frame manually. Instead, the system estimates the current progress of the movement using "
            "continuous values derived from joint angles. This is conceptually similar to in-between generation in "
            "animation, where intermediate states are estimated from surrounding key poses.",
            "A concrete implementation of this idea appears in the use of numerical interpolation to map movement "
            "angles to a progress percentage. When a joint angle moves from the lower threshold to the upper "
            "threshold, the system converts that change into a 0 to 100 percent progress value. This makes the "
            "exercise easier to visualize and provides a direct animation-oriented interpretation of how far the "
            "user has advanced from one pose to another.",
            ("subheading", "4.4 Temporal Continuity and Motion State Transition"),
            "Animation is fundamentally about change over time, not about isolated images. The project reflects "
            "this by evaluating movement across consecutive frames and maintaining a stage variable that stores the "
            "current motion state. A repetition is counted only when the body moves through the expected order of "
            "states. This resembles temporal continuity in animation, where the meaning of a pose depends on how "
            "it evolves over time rather than on one frame alone.",
            ("subheading", "4.5 Motion Capture Perspective"),
            "The project can also be interpreted as a lightweight markerless motion capture system. Instead of "
            "placing markers on the performer, the application uses a camera and pose estimation to recover a "
            "skeleton-like structure from the human body. This is relevant to computer animation because motion "
            "capture is a major method for transferring human performance into digital form. While the project does "
            "not drive a full 3D character, it demonstrates the same foundational idea of representing real-world "
            "movement as skeletal motion data.",
            ("subheading", "4.6 Readability of Motion and Feedback Design"),
            "Animation is also concerned with readability: the audience should be able to understand what motion is "
            "happening and how complete the action is. The project addresses this by overlaying the current stage, "
            "count, angle, and progress percentage on the video feed. The visual gauge acts like a compact motion "
            "timeline, helping the user see whether the movement is still near its starting pose or is approaching "
            "the target pose. This transforms raw motion data into interpretable animation-style feedback.",
        ]),
        ("5. Supporting Concepts from Computer Vision", [
            "Although the report emphasizes animation, computer vision provides the sensing layer that makes the "
            "system operational. The camera captures frames in real time, and MediaPipe Pose estimates body "
            "landmarks for each frame. OpenCV is used for image processing, coordinate handling, and live overlay "
            "rendering. The visibility values of landmarks help the program decide which side of the body is more "
            "reliably observed, allowing it to analyze the clearer arm or leg when occlusion occurs.",
            "The system then computes geometric relationships such as angles between three joints. These angles "
            "serve as the measurable basis for recognizing movement states. Threshold-based logic is used to "
            "classify whether the user is in a lower, upper, holding, or adjustment phase. In short, computer "
            "vision detects the motion, while computer animation provides the stronger conceptual framework for "
            "interpreting it.",
        ]),
        ("6. Exercise Set and Basic Instructions", [
            ("subheading", "Bicep Curl"),
            "Hold a dumbbell at your side, keep the upper arm relatively stable, curl the weight upward by "
            "bending the elbow, then lower it in a controlled manner. The system tracks elbow flexion and "
            "extension to detect a full repetition.",
            ("subheading", "Shoulder Press"),
            "Start with the weights around shoulder level, press both arms upward until the elbows are more "
            "extended, then bring the weights back down under control. The system interprets the lifting and "
            "lowering phases through arm angle changes.",
            ("subheading", "Dumbbell Side Lateral Raise"),
            "Begin with the arms near the sides of the body, raise the arms outward to approximately shoulder "
            "height while keeping the elbows mostly extended, and then lower the arms smoothly. This exercise "
            "strongly reflects the animation idea of moving from a start pose to a side-raised end pose with a "
            "continuous interpolated transition in between.",
            ("subheading", "Squat"),
            "Stand upright with the feet planted, bend the knees and hips to lower the body, then return to "
            "standing. The program analyzes the leg chain to estimate movement depth and detect a completed cycle.",
            ("subheading", "Plank"),
            "Hold the body in a straight supported position, maintain alignment from shoulders through hips to "
            "ankles, and avoid collapsing or lifting the torso excessively. Instead of repetition counting, the "
            "system mainly evaluates posture quality and holding time.",
            ("subheading", "High Knees"),
            "Run in place while alternately lifting the knees upward with a quick rhythm. The system tracks the "
            "alternating leg motion and detects the repeated lifting pattern over time.",
        ]),
        ("7. Implementation Summary", [
            "The codebase organizes exercise logic into separate classes, each inheriting from a common exercise "
            "base class. This design allows each movement to define its own thresholds, state transitions, and "
            "display behavior while still fitting into a shared camera and interface pipeline. The web application "
            "exposes exercise selection and reset controls, while the camera module manages frame acquisition, "
            "pose detection, motion analysis, and overlay rendering.",
            "A notable implementation detail is the repeated use of interpolation when converting measured angles "
            "into progress values for the on-screen gauge. This is a practical example of animation knowledge "
            "embedded in software behavior: the system is not only detecting a pose but also estimating where the "
            "current frame lies between major motion states.",
        ]),
        ("8. Results and Discussion", [
            "The project demonstrates that animation concepts can contribute directly to interactive motion "
            "analysis. By treating exercise performance as movement between key poses, the system can provide "
            "intuitive feedback that is more meaningful than a simple yes or no classification. Users receive "
            "information about stage, progress, and repetition count, which improves clarity and supports "
            "self-correction during exercise.",
            "The strongest contribution from the computer animation perspective is the interpretation of body "
            "movement as skeletal motion with in-between estimation. The strongest contribution from computer "
            "vision is the automatic acquisition of landmarks from live camera input. Together, they create a "
            "practical demonstration of how animation theory can enhance the understanding of human motion in "
            "real-time systems.",
        ]),
        ("9. Conclusion", [
            "This project is a meaningful application of both computer vision and computer animation, with "
            "primary emphasis on animation concepts. The system uses a skeletal body representation, pose-based "
            "reasoning, interpolation between movement states, and motion capture style interpretation to analyze "
            "exercise performance. Rather than viewing the problem only as recognition from images, the project "
            "treats it as the analysis of articulated motion over time. This makes the project highly relevant to "
            "the goals of a Computer Animation course.",
        ]),
        ("10. Future Improvements", [
            ("bullet", "Connect the estimated skeleton to a 2D or 3D animated character so that the user can see a digital avatar mirror the captured movement."),
            ("bullet", "Extend interpolation from simple progress mapping to smoother motion curves that reflect acceleration and deceleration similar to animation easing."),
            ("bullet", "Store landmark sequences for playback and motion comparison, enabling deeper motion study and performance review."),
            ("bullet", "Expand the exercise library and define more detailed pose checkpoints for advanced motion evaluation."),
        ]),
        ("References", [
            ("bullet", "Bradski, G. (2000). The OpenCV Library. Dr. Dobb's Journal of Software Tools."),
            ("bullet", "Google MediaPipe Team. MediaPipe Pose documentation and pose landmark estimation resources."),
            ("bullet", "Parent, R. (2012). Computer Animation: Algorithms and Techniques. Morgan Kaufmann."),
            ("bullet", "Watt, A., and Watt, M. (1992). Advanced Animation and Rendering Techniques. Addison-Wesley."),
            ("bullet", "Menache, A. (2010). Understanding Motion Capture for Computer Animation and Video Games. Morgan Kaufmann."),
        ]),
    ]

    for heading, content in sections:
        body.append(paragraph_xml(heading, style="Heading1", page_break_before=True))
        for item in content:
            if isinstance(item, tuple):
                kind, value = item
                if kind == "bullet":
                    body.append(bullet_xml(value))
                elif kind == "subheading":
                    body.append(paragraph_xml(value, style="Heading2"))
            else:
                body.append(paragraph_xml(item))

    body.append(section_properties_xml())
    return "".join(body)


def section_properties_xml():
    return (
        "<w:sectPr>"
        "<w:pgSz w:w=\"12240\" w:h=\"15840\"/>"
        "<w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" "
        "w:header=\"720\" w:footer=\"720\" w:gutter=\"0\"/>"
        "</w:sectPr>"
    )


def document_xml():
    body_xml = build_document_body()
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" "
        "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
        "xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
        "xmlns:m=\"http://schemas.openxmlformats.org/officeDocument/2006/math\" "
        "xmlns:v=\"urn:schemas-microsoft-com:vml\" "
        "xmlns:wp14=\"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing\" "
        "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
        "xmlns:w10=\"urn:schemas-microsoft-com:office:word\" "
        "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
        "xmlns:wpg=\"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup\" "
        "xmlns:wpi=\"http://schemas.microsoft.com/office/word/2010/wordprocessingInk\" "
        "xmlns:wne=\"http://schemas.microsoft.com/office/word/2006/wordml\" "
        "xmlns:wps=\"http://schemas.microsoft.com/office/word/2010/wordprocessingShape\" "
        "mc:Ignorable=\"w14 wp14\">"
        f"<w:body>{body_xml}</w:body>"
        "</w:document>"
    )


def styles_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:after="120"/></w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="32"/>
      <w:szCs w:val="32"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:after="80"/></w:pPr>
    <w:rPr>
      <w:sz w:val="26"/>
      <w:szCs w:val="26"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="CoverTitle">
    <w:name w:val="Cover Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="160" w:after="120"/></w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="36"/>
      <w:szCs w:val="36"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="CoverSubtitle">
    <w:name w:val="Cover Subtitle"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:after="120"/></w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="30"/>
      <w:szCs w:val="30"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="240" w:after="120"/></w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="30"/>
      <w:szCs w:val="30"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="160" w:after="80"/></w:pPr>
    <w:rPr>
      <w:b/>
      <w:sz w:val="26"/>
      <w:szCs w:val="26"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Quote">
    <w:name w:val="Quote"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr><w:spacing w:before="120" w:after="120"/></w:pPr>
    <w:rPr>
      <w:i/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph">
    <w:name w:val="List Paragraph"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:ind w:left="720" w:hanging="360"/>
      <w:spacing w:after="40"/>
    </w:pPr>
  </w:style>
</w:styles>
"""


def numbering_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="0">
    <w:multiLevelType w:val="singleLevel"/>
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/>
      <w:numFmt w:val="bullet"/>
      <w:lvlText w:val="•"/>
      <w:lvlJc w:val="left"/>
      <w:pPr>
        <w:ind w:left="720" w:hanging="360"/>
      </w:pPr>
      <w:rPr>
        <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/>
      </w:rPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1">
    <w:abstractNumId w:val="0"/>
  </w:num>
</w:numbering>
"""


def content_types_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""


def package_rels_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


def document_rels_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>
"""


def core_xml():
    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Computer Animation Project Report</dc:title>
  <dc:subject>Real-Time Exercise Tracking System</dc:subject>
  <dc:creator>{escape(AUTHOR_1)}</dc:creator>
  <cp:keywords>computer animation, computer vision, exercise tracking, MediaPipe, OpenCV</cp:keywords>
  <dc:description>Formal course project report in English.</dc:description>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{created}</dcterms:modified>
</cp:coreProperties>
"""


def app_xml():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Office Word</Application>
  <DocSecurity>0</DocSecurity>
  <ScaleCrop>false</ScaleCrop>
  <Company></Company>
  <LinksUpToDate>false</LinksUpToDate>
  <SharedDoc>false</SharedDoc>
  <HyperlinksChanged>false</HyperlinksChanged>
  <AppVersion>16.0000</AppVersion>
</Properties>
"""


def build_docx(output_path: Path):
    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types_xml())
        docx.writestr("_rels/.rels", package_rels_xml())
        docx.writestr("docProps/core.xml", core_xml())
        docx.writestr("docProps/app.xml", app_xml())
        docx.writestr("word/document.xml", document_xml())
        docx.writestr("word/styles.xml", styles_xml())
        docx.writestr("word/numbering.xml", numbering_xml())
        docx.writestr("word/_rels/document.xml.rels", document_rels_xml())


if __name__ == "__main__":
    output_path = Path(OUTPUT_FILE)
    build_docx(output_path)
    print(f"Generated {output_path}")
