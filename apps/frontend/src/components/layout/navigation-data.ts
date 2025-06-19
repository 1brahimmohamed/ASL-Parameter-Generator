import {
    IconBrandGithub,
    IconFileTypeDoc,
    IconSitemap,
    IconUpload,
    IconReport,
    IconExclamationCircle,
    IconAlertTriangle
} from "@tabler/icons-react"

const NavData = {
    navMain: [
        {
            title: "Upload",
            url: "/",
            icon: IconUpload,
        },
        {
            title: "Report",
            url: "/report",
            icon: IconReport,
        },
        {
            title: "Errors",
            url: "/report/errors",
            icon: IconExclamationCircle,
        },
        {
            title: "Warnings",
            url: "/report/warnings",
            icon: IconAlertTriangle,
        }
    ],
    navSecondary: [
        {
            title: "Documentation",
            url: "https://docs.page/1brahimmohamed/ASL-Parameter-Generator",
            icon: IconFileTypeDoc,
        },
        {
            title: "Github Repository",
            url: "https://github.com/1brahimmohamed/ASL-Parameter-Generator",
            icon: IconBrandGithub,
        },
        {
            title: "OSIPI TF 4.1: ASL Lexicon",
            url: "https://osipi.ismrm.org/task-forces/tf4-1/",
            icon: IconSitemap,
        },
    ],
}

export default NavData