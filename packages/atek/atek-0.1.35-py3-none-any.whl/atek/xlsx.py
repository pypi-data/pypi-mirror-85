# %% imports
import pandas as pd
import toolz.curried as tz
from pathlib import Path
import atek
from typing import Union, Dict, Optional
from dataclasses import dataclass, asdict
from fnmatch import fnmatch
import xlsxwriter.utility as xlcell

__all__ = ["xlformat", "to_xlsx", "XLCell", "XLRange", "data_range"]

# %% calc_column_width
def calc_column_width(data: pd.DataFrame, min_width: int=10, max_width: int=50
    ) -> Dict[str,int]:
    """Uses converts values to strings and gets the max length of all values
    and column names by column."""
    value_width = {
        col: data[col]
            .apply(lambda x: len(str(x)))
            .max()
        for col in data.columns
    }
    header_width = {col: len(col) for col in data.columns}
    min_width = {col: min_width for col in data.columns}
    max_width = {col: max_width for col in data.columns}
    width = tz.pipe(
        tz.merge_with(
            max
            ,value_width
            ,header_width
            ,min_width
        )
        ,lambda d: tz.merge_with(min, d, max_width)
    )
    return width

# calc_column_width(data, 4, 20)


# %% Codes
Codes = Dict[str, Union[str,int]]
# %% XLFormat
@dataclass(frozen=True)
class XLFormat:
    pattern: str
    codes: Codes


# %% ColFormat
@dataclass(frozen=True)
class ColFormat:
    header_codes: Codes
    value_codes: Codes


# %% XLPos
@dataclass(frozen=True)
class XLCell:
    row: int=0
    col: int=0
    row_abs: bool=False
    col_abs: bool=False

    @classmethod
    def from_cell(cls, cell: str):
        row, col, row_abs, col_abs = xlcell.xl_cell_to_rowcol_abs(cell)
        return cls(row, col, row_abs, col_abs)

    @classmethod
    def from_rowcol(cls, row: int, col: int, row_abs: bool, col_abs: bool):
        return cls(row, col, row_abs, col_abs)

    @property
    def cell(self) -> str:
        return xlcell.xl_rowcol_to_cell(
            self.row,
            self.col,
            self.row_abs,
            self.col_abs
        )

    @property
    def ref(self) -> str:
        return self.cell

    @property
    def col_name(self) -> str:
        return xlcell.xl_col_to_name(self.col, self.col_abs)

    def evolve(self, **kwargs) -> "XLCell":
        me = asdict(self)
        new = {
            **me,
            **{k: v for k, v in kwargs.items() if k in me}
        }
        return self.from_rowcol(**new)

    def __add__(self, other: "XLCell") -> "XLCell":
        return self.from_rowcol(
            self.row + other.row,
            self.col + other.col,
            self.row_abs,
            self.col_abs
        )

    def __sub__(self, other: "XLCell") -> "XLCell":
        return self.from_rowcol(
            self.row - other.row,
            self.col - other.col,
            self.row_abs,
            self.col_abs
        )

    def __call__(self) -> str:
        return self.cell


# %% XLRange
@dataclass(frozen=True)
class XLRange:
    cell1: XLCell
    cell2: XLCell

    @classmethod
    def from_rowcol(cls, row: int, col: int, row2:int, col2: int):
        return cls(
            XLCell(row, col),
            XLCell(row2, col2)
        )

    @classmethod
    def from_rowcol_abs(cls, row: int, col: int, row_abs: bool, col_abs: bool,
        row2: int, col2: int, row2_abs: bool, col2_abs: bool):
        return cls(
            XLCell(row, col, row_abs, col_abs),
            XLCell(row2, col2, row2_abs, col2_abs),
        )

    @classmethod
    def from_cells(cls, cell1: str, cell2: str):
        return cls(
            XLCell.from_cell(cell1),
            XLCell.from_cell(cell2)
        )

    @classmethod
    def from_ref(cls, ref: str):
        cell1, cell2 = ref.split(":")
        return cls.from_cells(cell1, cell2)

    @property
    def ref(self) -> str:
        return f"{self.cell1.cell}:{self.cell2.cell}"

    @property
    def columns(self) -> str:
        return f"{self.cell1.col_name}:{self.cell2.col_name}"

    def evolve(self, **kwargs):
        cell1 = asdict(self.cell1)
        cell2 = asdict(self.cell2)
        args1 = {
            k.replace("cell1_", ""): v
            for k, v in kwargs.items()
            if k.replace("cell1_", "") in cell1 and "cell1_" in k
        }
        args2 = {
            k.replace("cell2_", ""): v
            for k, v in kwargs.items()
            if k.replace("cell2_", "") in cell2 and "cell2_" in k
        }
        new1 = {**cell1, **args1}
        new2 = {**cell2, **args2}
        new2 = {
            k.replace("row", "row2").replace("col", "col2")
            : v for k, v in new2.items()
        }
        return self.from_rowcol_abs(**new1, **new2)

# %% xlformat
def xlformat(pattern: str, **kwargs) -> XLFormat:
    return XLFormat(pattern, kwargs)


# %% match_formats
def match_formats(data: pd.DataFrame, *formats: XLFormat) -> Dict[str,XLFormat]:
    matches = {}
    for col in data.columns:
        for fmt in formats:
            if col not in matches:
                pass
            if fnmatch(col, fmt.pattern):
                matches[col] = fmt
    return matches


# %% data_range
def data_range(data: pd.DataFrame, start: XLCell=XLCell(0, 0)) -> XLRange:
    """Returns the XLRange given the size of 'data' and 'start'."""
    rows, columns = data.shape

    # -1 from columns to make it 0-based, rows does not need this due to
    # having to account for header row
    end_cell = XLCell(rows, columns - 1)
    table_range = XLRange(start, start + end_cell)
    return table_range


# %%
def default_header_codes(dtype: str="object") -> Codes:
    align = (
        "left" if dtype == "object" else
        "left" if "date" in dtype else
        "right"
    )
    return {
        "align": align,
        "valign": "bottom",
        "bold": True,
        "text_wrap": True,
    }


def default_value_codes(dtype: str="object") -> Codes:
    num_format = (
        "" if dtype == "object" else
        "#,##0" if "int" in dtype else
        "#,##0.00" if "float" in dtype else
        "yyyy-mm-dd" if "date" in dtype else
        ""
    )
    align = (
        "left" if dtype == "object" else
        "left" if "date" in dtype else
        "right"
    )
    return {
        "align": align,
        "valign": "top",
        "num_format": num_format,
        "bold": False,
        "text_wrap": True,
    }


# %% column_formats
def column_formats(data: pd.DataFrame, *formats: XLFormat) -> Dict[str, ColFormat]:
    """Return a XLFormat object for each column in 'data'."""
    # Get matched formats
    matched = match_formats(data, *formats)

    result = {}
    # Get data type and set default format for all columns
    for header in data.columns:
        dtype = data[header].dtype.name.lower()
        value_fmt = default_value_codes(dtype)
        header_fmt = default_header_codes(dtype)

        # Override default formats with matched if they exist
        codes = matched[header].codes if header in matched else value_fmt
        result[header] = ColFormat(
            header_fmt,
            {**value_fmt, **codes},
        )
    return result


# %% to_xlsx
def to_xlsx(data: pd.DataFrame, file: pd.ExcelWriter, sheet_name: str,
    *formats: XLFormat, index: bool=False, start: XLCell=XLCell(0, 0),
    min_col_width: int=10, max_col_width: int=50,
    header_format: Optional[Codes]=None, make_table: bool=True,
    freeze_cell: XLCell=XLCell(1, 0)) -> XLRange:
    """Writes 'data' at 'start' and formats the columns."""

    # Get reference to sheet and workbook
    wb = file.book
    ws = wb.add_worksheet(sheet_name)
    table_range = data_range(data, start)

    # verify engine is xlsxwriter
    file.engine = "xlsxwriter"

    # Get column widths
    widths = calc_column_width(data, min_col_width, max_col_width)

    # Get formats
    fmts = column_formats(data, *formats)

    # Write data
    for idx, header in enumerate(data.columns):
        # Write Header
        header_format = (
            {**fmts[header].header_codes, **header_format}
            if header_format else
            fmts[header].header_codes
        )

        header_fmt = wb.add_format(header_format)
        ws.write_string(start.row, idx, header, header_fmt)

        # Write values
        value_fmt = wb.add_format(fmts[header].value_codes)
        ws.write_column(
            row=start.row + 1,
            col=idx,
            data=data[header],
            cell_format=value_fmt
        )

        # Set column width
        ws.set_column(idx, idx, widths[header])
        print(f"Wrote data for {header}")

    # Freeze panes
    freeze = start + freeze_cell
    ws.freeze_panes(freeze.row, freeze.col)
    print("Froze panes")

    # Add table
    if make_table:
        ws.add_table(
            table_range.ref,
            {
                "name": sheet_name.replace(" ", "_"),
                "header_row": True,
                "autofilter": False,
                "banded_rows": True,
                "style": "Table Style Light 1",
                "columns": [{"header": col} for col in data.columns],
            },
        )
        print("added table")

    return table_range
