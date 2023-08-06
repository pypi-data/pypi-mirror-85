export var rawSpanKeys = new Set([
    'trace_id',
    'parent_span_id',
    'span_id',
    'start_timestamp',
    'timestamp',
    'same_process_as_parent',
    'op',
    'description',
    'status',
    'data',
    'tags',
]);
export var TickAlignment;
(function (TickAlignment) {
    TickAlignment[TickAlignment["Left"] = 0] = "Left";
    TickAlignment[TickAlignment["Right"] = 1] = "Right";
    TickAlignment[TickAlignment["Center"] = 2] = "Center";
})(TickAlignment || (TickAlignment = {}));
//# sourceMappingURL=types.jsx.map