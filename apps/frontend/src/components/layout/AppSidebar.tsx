"use client"

import * as React from "react"
import {
  IconCamera,
  IconChartBar,
  IconDashboard,
  IconDatabase,
  IconFileAi,
  IconFileDescription,
  IconFileWord,
  IconFolder,
  IconHelp,
  IconInnerShadowTop,
  IconListDetails,
  IconReport,
  IconSearch,
  IconSettings,
  IconUsers,
} from "@tabler/icons-react"

import Image from "next/image"
import Link from "next/link"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

const AppSidebar = ({ ...props }: React.ComponentProps<typeof Sidebar>) => {
  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-2 h-14">
              <Link href="/">
                <Image
                  src="/logo/full_logo.webp"
                  alt="OSIPI Logo"
                  className="inline dark:hidden"
                  width={250}
                  height={72}
                />

                 <Image
                  src="/logo/full_logo_white.webp"
                  alt="OSIPI Logo"
                  className="hidden dark:inline"
                  width={250}
                  height={72}
                />
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        {/* CONTENT HERE  */}
      </SidebarContent>
      <SidebarFooter>
       
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar
