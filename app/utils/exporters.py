"""Utility generica per esportare collezioni di record in vari formati (JSON, XLSX, CSV)."""
from __future__ import annotations

import csv
import io
import json
from datetime import date, datetime
from enum import Enum
from typing import Any, Mapping, Optional, Sequence

from flask import Response, request, send_file
from openpyxl import Workbook

Record = Mapping[str, Any]
ScalarValue = Optional[str | int | float | bool]


class ExportFormat(str, Enum):
    """Formati di export supportati dalla utility."""
    JSON = "json"
    XLSX = "xlsx"
    CSV = "csv"

    @classmethod
    def from_string(cls, value: Optional[str], default: "ExportFormat" = None) -> "ExportFormat":
        """Converte il parametro `?format=` della request nell'enum corrispondente."""
        if not value:
            return default if default is not None else cls.JSON
        try:
            return cls(value.lower())
        except ValueError as exc:
            supported = ", ".join(f.value for f in cls)
            raise ValueError(f"Formato di export '{value}' non supportato. Formati validi: {supported}") from exc


def resolve_export_format(default: ExportFormat = ExportFormat.XLSX) -> ExportFormat:
    """Legge `?format=` dalla request Flask corrente e lo converte in ExportFormat."""
    return ExportFormat.from_string(request.args.get("format"), default=default)


def _flatten_value(value: Any) -> ScalarValue:
    """Converte valori non scalari (dict/list/date) in tipi compatibili con Excel/CSV."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return json.dumps(value, default=str, ensure_ascii=False)


def _collect_columns(records: Sequence[Record], columns: Optional[Sequence[str]]) -> list[str]:
    """Determina l'ordine delle colonne: quelle esplicite oppure l'unione ordinata delle chiavi trovate."""
    if columns:
        return list(columns)
    seen: dict[str, None] = {}
    for record in records:
        for key in record.keys():
            seen.setdefault(key, None)
    return list(seen.keys())


def export_records(
    records: Sequence[Record],
    fmt: ExportFormat,
    filename: str = "export",
    columns: Optional[Sequence[str]] = None,
) -> Response:
    """Serializza una lista di record (dict-like) nel formato richiesto, pronta per l'invio al frontend."""
    if fmt is ExportFormat.JSON:
        return _to_json_response(records)
    if fmt is ExportFormat.CSV:
        return _to_csv_response(records, filename, columns)
    if fmt is ExportFormat.XLSX:
        return _to_xlsx_response(records, filename, columns)
    raise ValueError(f"Formato di export non supportato: {fmt}")


def _to_json_response(records: Sequence[Record]) -> Response:
    body = json.dumps(list(records), default=str, ensure_ascii=False)
    return Response(body, mimetype="application/json")


def _to_csv_response(records: Sequence[Record], filename: str, columns: Optional[Sequence[str]]) -> Response:
    cols = _collect_columns(records, columns)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=cols, extrasaction="ignore")
    writer.writeheader()
    for record in records:
        writer.writerow({key: _flatten_value(record.get(key)) for key in cols})

    response = Response(buffer.getvalue(), mimetype="text/csv")
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}.csv"'
    return response


def _to_xlsx_response(records: Sequence[Record], filename: str, columns: Optional[Sequence[str]]) -> Response:
    cols = _collect_columns(records, columns)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Export"
    sheet.append(cols)
    for record in records:
        sheet.append([_flatten_value(record.get(key)) for key in cols])

    buffer = io.BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{filename}.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
