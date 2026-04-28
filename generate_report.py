from datetime import date

from fpdf import FPDF
from fpdf.enums import XPos, YPos


OUTPUT_FILE = "Computer_Animation_Project_Report.pdf"
UNIVERSITY_NAME = "[University Name]"
FACULTY_NAME = "[Faculty / Department]"
COURSE_NAME = "Computer Animation"
COURSE_CODE = "[Course Code]"
INSTRUCTOR_NAME = "[Instructor Name]"
SEMESTER_INFO = "[Semester / Academic Year]"
AUTHOR_1 = "[Your Name] ([Student ID])"
AUTHOR_2 = "[Teammate Name] ([Student ID])"


class ReportPDF(FPDF):
    @property
    def text_width(self):
        return self.w - self.l_margin - self.r_margin

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("Times", "I", 10)
        self.set_text_color(90, 90, 90)
        self.set_x(self.l_margin)
        self.cell(0, 8, "Computer Animation Project Report", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
        self.ln(2)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font("Times", "I", 10)
        self.set_text_color(90, 90, 90)
        self.cell(0, 8, f"Page {self.page_no()}", 0, new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")

    def chapter_title(self, number, title):
        self.set_text_color(20, 20, 20)
        self.set_font("Times", "B", 16)
        heading = f"{number}. {title}" if number else title
        self.set_x(self.l_margin)
        self.cell(0, 10, heading, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.set_draw_color(50, 50, 50)
        self.set_line_width(0.4)
        x = self.get_x()
        y = self.get_y()
        self.line(10, y, 200, y)
        self.ln(4)

    def subsection_title(self, title):
        self.set_text_color(30, 30, 30)
        self.set_font("Times", "B", 13)
        self.set_x(self.l_margin)
        self.cell(0, 8, title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.ln(1)

    def paragraph(self, text):
        self.set_text_color(20, 20, 20)
        self.set_font("Times", "", 12)
        self.set_x(self.l_margin)
        self.multi_cell(self.text_width, 7, text)
        self.ln(1)

    def bullet(self, text):
        self.set_text_color(20, 20, 20)
        self.set_font("Times", "", 12)
        self.set_x(self.l_margin)
        self.cell(6, 7, "-", 0, new_x=XPos.RIGHT, new_y=YPos.TOP)
        self.multi_cell(self.text_width - 6, 7, text)


def add_cover(pdf):
    pdf.add_page()
    pdf.set_fill_color(235, 239, 245)
    pdf.rect(12, 12, 186, 263, "DF")

    pdf.ln(20)
    pdf.set_font("Times", "B", 16)
    pdf.cell(0, 8, UNIVERSITY_NAME, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Times", "", 13)
    pdf.cell(0, 8, FACULTY_NAME, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.ln(20)
    pdf.set_text_color(30, 30, 30)
    pdf.set_font("Times", "B", 24)
    pdf.set_x(20)
    pdf.multi_cell(170, 12, "Real-Time Exercise Tracking System", 0, "C")
    pdf.set_font("Times", "B", 20)
    pdf.set_x(20)
    pdf.multi_cell(170, 11, "An Application of Computer Vision and Computer Animation", 0, "C")

    pdf.ln(12)
    pdf.set_font("Times", "", 14)
    pdf.set_x(20)
    pdf.multi_cell(170, 8, "Formal Project Report", 0, "C")
    pdf.set_x(20)
    pdf.multi_cell(170, 8, f"Course: {COURSE_NAME}", 0, "C")

    pdf.ln(22)
    pdf.set_font("Times", "B", 14)
    pdf.cell(0, 8, "Prepared by", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Times", "", 13)
    pdf.cell(0, 8, AUTHOR_1, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(0, 8, AUTHOR_2, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.ln(18)
    pdf.set_font("Times", "", 13)
    pdf.cell(0, 8, f"Course Code: {COURSE_CODE}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(0, 8, f"Instructor: {INSTRUCTOR_NAME}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(0, 8, f"Semester: {SEMESTER_INFO}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(0, 8, f"Submission Date: {date.today().strftime('%B %d, %Y')}", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.ln(36)
    pdf.set_font("Times", "I", 12)
    pdf.set_x(22)
    pdf.multi_cell(
        166,
        7,
        "This report documents the design and implementation of a real-time exercise "
        "tracking system that combines pose estimation, motion analysis, and animation-oriented "
        "movement interpretation.",
        0,
        "C",
    )


def add_preface(pdf):
    pdf.add_page()
    pdf.chapter_title("", "Preface")
    pdf.paragraph(
        "This report presents a two-member course project developed for Computer Animation. "
        "The project explores how movement analysis can be studied through the combined use of "
        "computer vision and computer animation. Although the system relies on computer vision to "
        "observe the user through a webcam, the conceptual focus of this report is intentionally "
        "placed on computer animation. The project interprets human exercise as a sequence of poses, "
        "transitions, and motion progressions rather than as isolated image frames."
    )
    pdf.paragraph(
        "The central idea is that each exercise can be described by a start pose, an end pose, and "
        "a continuous transition between them. This is directly aligned with animation practice, in "
        "which key poses define major movement states and interpolation estimates the in-between "
        "motion. MediaPipe landmarks act as a simplified skeleton, allowing the system to observe body "
        "joints in a manner related to motion capture and skeletal animation."
    )
    pdf.paragraph(
        "The following sections provide the project background, theoretical foundations, implementation "
        "summary, exercise descriptions, and conclusions. The discussion highlights how animation "
        "principles such as interpolation, key poses, state transitions, motion continuity, and skeletal "
        "representation are concretely applied in the project."
    )


def add_acknowledgements(pdf):
    pdf.add_page()
    pdf.chapter_title("", "Acknowledgements")
    pdf.paragraph(
        "We would like to express our sincere gratitude to the course instructor for guidance, academic "
        "support, and constructive feedback throughout the development of this project. We also appreciate "
        "the opportunity provided by the Computer Animation course to study motion not only as a visual "
        "phenomenon but also as a computable structure that can be interpreted, measured, and communicated "
        "through interactive systems."
    )
    pdf.paragraph(
        "This project was completed collaboratively by two students. The work reflects shared effort in "
        "conceptual design, implementation, testing, and report preparation."
    )


def add_abstract(pdf):
    pdf.add_page()
    pdf.chapter_title("", "Abstract")
    pdf.paragraph(
        "This project presents a real-time exercise tracking system developed as a course project for "
        "Computer Animation. The system combines computer vision and computer animation in order to "
        "capture, interpret, and evaluate human exercise movements from live webcam input. MediaPipe Pose "
        "is used to estimate body landmarks, while OpenCV supports real-time frame processing and visual "
        "feedback. Exercise-specific logic is implemented to detect movement stages, evaluate pose quality, "
        "and count completed repetitions."
    )
    pdf.paragraph(
        "The main academic contribution of the project lies in its animation-oriented interpretation of "
        "motion. Each exercise is modeled through a start pose, an end pose, and a continuous transition "
        "between them. This reflects core animation concepts such as skeletal representation, key poses, "
        "interpolation, temporal continuity, and motion capture. Rather than viewing the system only as a "
        "recognition task, the project treats body motion as articulated movement progressing through a "
        "sequence of meaningful states."
    )
    pdf.paragraph(
        "The final system supports six exercises: Bicep Curl, Shoulder Press, Dumbbell Side Lateral Raise, "
        "Squat, Plank, and High Knees. The project demonstrates that computer animation principles can be "
        "applied effectively beyond traditional content creation and can play an important role in the "
        "analysis of human movement in interactive applications."
    )


def add_contents(pdf):
    pdf.chapter_title("", "Table of Contents")
    items = [
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
    for item in items:
        pdf.bullet(item)
    pdf.ln(2)


def add_main_sections(pdf):
    pdf.chapter_title("1", "Introduction")
    pdf.paragraph(
        "The project is a real-time exercise tracking system implemented with Python, OpenCV, "
        "MediaPipe, and a web-based interface. The system receives video from a webcam, estimates "
        "body landmarks, computes joint relationships, and uses those measurements to evaluate "
        "exercise execution. It can switch between multiple exercise types and display live feedback "
        "such as repetition count, motion stage, and progress percentage."
    )
    pdf.paragraph(
        "From an animation perspective, the system is not merely recognizing a person in front of a "
        "camera. Instead, it is interpreting human motion as a structured sequence of poses linked by "
        "continuous transitions over time. This makes the project especially relevant to Computer "
        "Animation because it transforms observed movement into skeletal data, pose states, and "
        "interpolated motion progress."
    )

    pdf.chapter_title("2", "Project Objectives")
    pdf.bullet(
        "To design a real-time exercise tracking application that automatically analyzes body motion and "
        "provides understandable visual feedback."
    )
    pdf.bullet(
        "To demonstrate how computer animation principles such as skeletal representation, key poses, "
        "and interpolation can be applied to motion analysis."
    )
    pdf.bullet(
        "To integrate computer vision techniques for body landmark detection with animation-oriented "
        "reasoning about movement."
    )
    pdf.bullet(
        "To support multiple exercises and explain each movement through meaningful motion stages."
    )
    pdf.ln(1)

    pdf.chapter_title("3", "System Overview")
    pdf.paragraph(
        "The system consists of three main layers. The first layer is video acquisition and pose "
        "estimation, where webcam frames are processed and body landmarks are extracted. The second "
        "layer is exercise-specific motion analysis, where each exercise class interprets the landmark "
        "configuration according to its own movement rules. The third layer is user feedback, where the "
        "current exercise name, repetition count, stage, and motion percentage are displayed on the live "
        "video stream and the web dashboard."
    )
    pdf.paragraph(
        "This layered structure supports a modular interpretation of movement. Each exercise is modeled "
        "as a specific animation-like motion pattern with a clear beginning, progression, and completion. "
        "Because the exercise logic is encapsulated in separate modules, the project can be extended with "
        "new movements without redesigning the entire pipeline."
    )

    pdf.chapter_title("4", "Theoretical Foundation in Computer Animation")
    pdf.subsection_title("4.1 Skeletal Representation and Rig Analogy")
    pdf.paragraph(
        "MediaPipe represents the human body through landmarks located at key joints such as shoulders, "
        "elbows, wrists, hips, knees, ankles, and other body points. When these landmarks are connected, "
        "they form a simplified skeleton similar to the rig structure used in computer animation. In a "
        "traditional animation pipeline, a character rig defines how limbs are connected and how movement "
        "can be described through joints. In this project, the body landmarks play a comparable role by "
        "providing a structured articulation model for motion analysis."
    )
    pdf.subsection_title("4.2 Key Poses and Pose-to-Pose Thinking")
    pdf.paragraph(
        "Each exercise can be broken into major poses such as down, up, hold, or adjust. This is closely "
        "related to pose-to-pose animation, where an animator first defines important key poses and then "
        "constructs the in-between movement. For example, a bicep curl has a clear lowered-arm pose and "
        "a flexed-arm pose. A squat has an upright standing pose and a lowered pose at the bottom of the "
        "movement. By detecting when the body reaches these major states, the project applies the same "
        "logic used to organize movement in animation."
    )
    pdf.subsection_title("4.3 Interpolation Between Start and End Poses")
    pdf.paragraph(
        "Interpolation is one of the most important animation concepts in this project. For every supported "
        "exercise, there is a start pose and an end pose. The motion between them does not need to be defined "
        "frame by frame manually. Instead, the system estimates the current progress of the movement using "
        "continuous values derived from joint angles. This is conceptually similar to in-between generation in "
        "animation, where intermediate states are estimated from surrounding key poses."
    )
    pdf.paragraph(
        "A concrete implementation of this idea appears in the use of numerical interpolation to map movement "
        "angles to a progress percentage. When a joint angle moves from the lower threshold to the upper "
        "threshold, the system converts that change into a 0 to 100 percent progress value. This makes the "
        "exercise easier to visualize and provides a direct animation-oriented interpretation of how far the "
        "user has advanced from one pose to another."
    )
    pdf.subsection_title("4.4 Temporal Continuity and Motion State Transition")
    pdf.paragraph(
        "Animation is fundamentally about change over time, not about isolated images. The project reflects "
        "this by evaluating movement across consecutive frames and maintaining a stage variable that stores the "
        "current motion state. A repetition is counted only when the body moves through the expected order of "
        "states. This resembles temporal continuity in animation, where the meaning of a pose depends on how it "
        "evolves over time rather than on one frame alone."
    )
    pdf.subsection_title("4.5 Motion Capture Perspective")
    pdf.paragraph(
        "The project can also be interpreted as a lightweight markerless motion capture system. Instead of "
        "placing markers on the performer, the application uses a camera and pose estimation to recover a "
        "skeleton-like structure from the human body. This is relevant to computer animation because motion "
        "capture is a major method for transferring human performance into digital form. While the project does "
        "not drive a full 3D character, it demonstrates the same foundational idea of representing real-world "
        "movement as skeletal motion data."
    )
    pdf.subsection_title("4.6 Readability of Motion and Feedback Design")
    pdf.paragraph(
        "Animation is also concerned with readability: the audience should be able to understand what motion is "
        "happening and how complete the action is. The project addresses this by overlaying the current stage, "
        "count, angle, and progress percentage on the video feed. The visual gauge acts like a compact motion "
        "timeline, helping the user see whether the movement is still near its starting pose or is approaching "
        "the target pose. This transforms raw motion data into interpretable animation-style feedback."
    )

    pdf.chapter_title("5", "Supporting Concepts from Computer Vision")
    pdf.paragraph(
        "Although the report emphasizes animation, computer vision provides the sensing layer that makes the "
        "system operational. The camera captures frames in real time, and MediaPipe Pose estimates body "
        "landmarks for each frame. OpenCV is used for image processing, coordinate handling, and live overlay "
        "rendering. The visibility values of landmarks help the program decide which side of the body is more "
        "reliably observed, allowing it to analyze the clearer arm or leg when occlusion occurs."
    )
    pdf.paragraph(
        "The system then computes geometric relationships such as angles between three joints. These angles "
        "serve as the measurable basis for recognizing movement states. Threshold-based logic is used to classify "
        "whether the user is in a lower, upper, holding, or adjustment phase. In short, computer vision detects "
        "the motion, while computer animation provides the stronger conceptual framework for interpreting it."
    )

    pdf.chapter_title("6", "Exercise Set and Basic Instructions")
    exercises = [
        (
            "Bicep Curl",
            "Hold a dumbbell at your side, keep the upper arm relatively stable, curl the weight upward by "
            "bending the elbow, then lower it in a controlled manner. The system tracks elbow flexion and "
            "extension to detect a full repetition.",
        ),
        (
            "Shoulder Press",
            "Start with the weights around shoulder level, press both arms upward until the elbows are more "
            "extended, then bring the weights back down under control. The system interprets the lifting and "
            "lowering phases through arm angle changes.",
        ),
        (
            "Dumbbell Side Lateral Raise",
            "Begin with the arms near the sides of the body, raise the arms outward to approximately shoulder "
            "height while keeping the elbows mostly extended, and then lower the arms smoothly. This exercise "
            "strongly reflects the animation idea of moving from a start pose to a side-raised end pose with a "
            "continuous interpolated transition in between.",
        ),
        (
            "Squat",
            "Stand upright with the feet planted, bend the knees and hips to lower the body, then return to "
            "standing. The program analyzes the leg chain to estimate movement depth and detect a completed cycle.",
        ),
        (
            "Plank",
            "Hold the body in a straight supported position, maintain alignment from shoulders through hips to "
            "ankles, and avoid collapsing or lifting the torso excessively. Instead of repetition counting, the "
            "system mainly evaluates posture quality and holding time.",
        ),
        (
            "High Knees",
            "Run in place while alternately lifting the knees upward with a quick rhythm. The system tracks the "
            "alternating leg motion and detects the repeated lifting pattern over time.",
        ),
    ]
    for name, description in exercises:
        pdf.subsection_title(name)
        pdf.paragraph(description)

    pdf.chapter_title("7", "Implementation Summary")
    pdf.paragraph(
        "The codebase organizes exercise logic into separate classes, each inheriting from a common exercise base "
        "class. This design allows each movement to define its own thresholds, state transitions, and display "
        "behavior while still fitting into a shared camera and interface pipeline. The web application exposes "
        "exercise selection and reset controls, while the camera module manages frame acquisition, pose detection, "
        "motion analysis, and overlay rendering."
    )
    pdf.paragraph(
        "A notable implementation detail is the repeated use of interpolation when converting measured angles into "
        "progress values for the on-screen gauge. This is a practical example of animation knowledge embedded in "
        "software behavior: the system is not only detecting a pose but also estimating where the current frame lies "
        "between major motion states."
    )

    pdf.chapter_title("8", "Results and Discussion")
    pdf.paragraph(
        "The project demonstrates that animation concepts can contribute directly to interactive motion analysis. "
        "By treating exercise performance as movement between key poses, the system can provide intuitive feedback "
        "that is more meaningful than a simple yes or no classification. Users receive information about stage, "
        "progress, and repetition count, which improves clarity and supports self-correction during exercise."
    )
    pdf.paragraph(
        "The strongest contribution from the computer animation perspective is the interpretation of body movement "
        "as skeletal motion with in-between estimation. The strongest contribution from computer vision is the "
        "automatic acquisition of landmarks from live camera input. Together, they create a practical demonstration "
        "of how animation theory can enhance the understanding of human motion in real-time systems."
    )

    pdf.chapter_title("9", "Conclusion")
    pdf.paragraph(
        "This project is a meaningful application of both computer vision and computer animation, with primary "
        "emphasis on animation concepts. The system uses a skeletal body representation, pose-based reasoning, "
        "interpolation between movement states, and motion capture style interpretation to analyze exercise "
        "performance. Rather than viewing the problem only as recognition from images, the project treats it as "
        "the analysis of articulated motion over time. This makes the project highly relevant to the goals of a "
        "Computer Animation course."
    )

    pdf.chapter_title("10", "Future Improvements")
    pdf.bullet(
        "Connect the estimated skeleton to a 2D or 3D animated character so that the user can see a digital avatar "
        "mirror the captured movement."
    )
    pdf.bullet(
        "Extend interpolation from simple progress mapping to smoother motion curves that reflect acceleration and "
        "deceleration similar to animation easing."
    )
    pdf.bullet(
        "Store landmark sequences for playback and motion comparison, enabling deeper motion study and performance review."
    )
    pdf.bullet(
        "Expand the exercise library and define more detailed pose checkpoints for advanced motion evaluation."
    )


def add_references(pdf):
    pdf.chapter_title("", "References")
    references = [
        "Bradski, G. (2000). The OpenCV Library. Dr. Dobb's Journal of Software Tools.",
        "Google MediaPipe Team. MediaPipe Pose documentation and pose landmark estimation resources.",
        "Parent, R. (2012). Computer Animation: Algorithms and Techniques. Morgan Kaufmann.",
        "Watt, A., and Watt, M. (1992). Advanced Animation and Rendering Techniques. Addison-Wesley.",
        "Menache, A. (2010). Understanding Motion Capture for Computer Animation and Video Games. Morgan Kaufmann.",
    ]
    for item in references:
        pdf.bullet(item)


def build_report():
    pdf = ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(15, 15, 15)
    pdf.alias_nb_pages()

    add_cover(pdf)
    add_preface(pdf)
    add_acknowledgements(pdf)
    add_abstract(pdf)
    add_contents(pdf)
    add_main_sections(pdf)
    add_references(pdf)

    pdf.output(OUTPUT_FILE)
    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    build_report()
