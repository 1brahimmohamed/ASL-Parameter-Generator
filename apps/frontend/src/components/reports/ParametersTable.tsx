"use client"

import React, {useState, useEffect} from "react"

import {
    ColumnDef,
    ColumnFiltersState,
    flexRender,
    getCoreRowModel,
    getFilteredRowModel,
    getSortedRowModel,
    SortingState,
    useReactTable,
    VisibilityState,
} from "@tanstack/react-table"
import {ArrowUpDown, ChevronDown, MoreHorizontal} from "lucide-react"

import {Button} from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuCheckboxItem,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {Input} from "@/components/ui/input"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"
import {useAppContext} from "@/providers/AppProvider";
import {mapAslParametersToTable} from "@/utils";

const data: Parameter[] = [
    {
        id: "1",
        parameter: "ImagePatientPosition",
        value: "HFS",
    },
    {
        id: "2",
        parameter: "ImageType",
        value: "ORIGINAL\\PRIMARY\\AXIAL\\CT",
    },
    {
        id: "3",
        parameter: "Modality",
        value: "CT",
    },
    {
        id: "4",
        parameter: "PatientID",
        value: "123456",
    },
    {
        id: "5",
        parameter: "StudyInstanceUID",
        value: "1.2.840.113619.2.55.3.604688.100.1.10000000000000000000",
    },
    {
        id: "6",
        parameter: "SeriesInstanceUID",
        value: "1.2.840.113619.2.55.3.604688.100.1.10000000000000000001",
    },
    {
        id: "7",
        parameter: "SOPInstanceUID",
        value: "1.2.840.113619.2.55.3.604688.100.1.10000000000000000002",
    },
    {
        id: "8",
        parameter: "StudyDate",
        value: "20231001",
    },
    {
        id: "9",
        parameter: "SeriesNumber",
        value: "1",
    },
    {
        id: "10",
        parameter: "InstanceNumber",
        value: "1",
    },
    {
        id: "11",
        parameter: "SliceThickness",
        value: "5.0",
    },
    {
        id: "12",
        parameter: "PixelSpacing",
        value: "0.5\\0.5",
    },
    {
        id: "13",
        parameter: "ImageOrientationPatient",
        value: "1\\0\\0\\0\\1\\0",
    },
    {
        id: "14",
        parameter: "ImagePositionPatient",
        value: "0\\0\\0",
    },
]


export type Parameter = {
    id: string
    parameter: string
    value: string
}

export const columns: ColumnDef<Parameter>[] = [
    {
        accessorKey: "parameter",
        header: ({column}) => {
            return (
                <Button
                    variant="ghost"
                    onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                >
                    Parameter<ArrowUpDown/>
                </Button>
            )
        },
        cell: ({row}) => <div>{row.getValue("parameter")}</div>,
    },
    {
        accessorKey: "value",
        header: "Value",
        cell: ({row}) => (
            <div className="capitalize">{row.getValue("value")}</div>
        ),
    },
    {
        id: "actions",
        enableHiding: false,
        cell: ({row}) => {
            const parameter = row.original as Parameter

            return (
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                            <span className="sr-only">Open menu</span>
                            <MoreHorizontal/>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem
                            onClick={() => navigator.clipboard.writeText(parameter.id)}
                        >
                            Copy parameter ID
                        </DropdownMenuItem>
                        <DropdownMenuSeparator/>
                        <DropdownMenuItem>View parameter details</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            )
        },
    },
]

export default function ParametersTable() {
    const [sorting, setSorting] = useState<SortingState>([])
    const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>(
        []
    )
    const [columnVisibility, setColumnVisibility] =
        useState<VisibilityState>({})
    const [rowSelection, setRowSelection] = useState({})
    const [tableData, setTableData] = useState<Parameter[]>(data);

    const {apiData} = useAppContext();

    useEffect(() => {
        if (apiData && apiData.asl_parameters) {
            console.log("API Data:", apiData.asl_parameters);
            console.log("M0 Data:", apiData.m0_parameters);
            const combinedData = [...apiData.asl_parameters, ...apiData.m0_parameters];
            const mappedData = mapAslParametersToTable(combinedData);
            console.log("Mapped Data:", mappedData);
            setTableData(mappedData);
        }
    }, [apiData]);


    const table = useReactTable({
        data: tableData,
        columns,
        onSortingChange: setSorting,
        onColumnFiltersChange: setColumnFilters,
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        onColumnVisibilityChange: setColumnVisibility,
        onRowSelectionChange: setRowSelection,
        state: {
            sorting,
            columnFilters,
            columnVisibility,
            rowSelection,
        },
    })

    return (
        <div className="flex flex-col gap-4 w-full overflow-hidden">
            <div className="flex items-center gap-2">
                <Input
                    placeholder="Filter Parameters..."
                    value={(table.getColumn("parameter")?.getFilterValue() as string) ?? ""}
                    onChange={(event) =>
                        table.getColumn("parameter")?.setFilterValue(event.target.value)
                    }
                    className="max-w-sm"
                />
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="outline" className="ml-auto shrink-0">
                            Columns <ChevronDown/>
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        {table
                            .getAllColumns()
                            .filter((column) => column.getCanHide())
                            .map((column) => {
                                return (
                                    <DropdownMenuCheckboxItem
                                        key={column.id}
                                        className="capitalize"
                                        checked={column.getIsVisible()}
                                        onCheckedChange={(value) =>
                                            column.toggleVisibility(!!value)
                                        }
                                    >
                                        {column.id}
                                    </DropdownMenuCheckboxItem>
                                )
                            })}
                    </DropdownMenuContent>
                </DropdownMenu>
            </div>
            <div className="rounded-md border h-full overflow-hidden">
                <div className="max-h-96 overflow-auto">
                    <Table className="w-full table-fixed">
                        <TableHeader className="bg-gray-100 dark:bg-secondary sticky top-0 z-10">
                            {table.getHeaderGroups().map((headerGroup) => (
                                <TableRow key={headerGroup.id}>
                                    {headerGroup.headers.map((header) => {
                                        return (
                                            <TableHead key={header.id} className="w-1/2">
                                                {header.isPlaceholder
                                                    ? null
                                                    : flexRender(
                                                        header.column.columnDef.header,
                                                        header.getContext()
                                                    )}
                                            </TableHead>
                                        )
                                    })}
                                </TableRow>
                            ))}
                        </TableHeader>
                        <TableBody>
                            {table.getRowModel().rows?.length ? (
                                table.getRowModel().rows.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        data-state={row.getIsSelected() && "selected"}
                                    >
                                        {row.getVisibleCells().map((cell) => (
                                            <TableCell key={cell.id} className="w-1/2">
                                                <div className="truncate">
                                                    {flexRender(
                                                        cell.column.columnDef.cell,
                                                        cell.getContext()
                                                    )}
                                                </div>
                                            </TableCell>
                                        ))}
                                    </TableRow>
                                ))
                            ) : (
                                <TableRow>
                                    <TableCell
                                        colSpan={columns.length}
                                        className="h-24 text-center"
                                    >
                                        No results.
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </div>
            </div>
        </div>
    )
}
