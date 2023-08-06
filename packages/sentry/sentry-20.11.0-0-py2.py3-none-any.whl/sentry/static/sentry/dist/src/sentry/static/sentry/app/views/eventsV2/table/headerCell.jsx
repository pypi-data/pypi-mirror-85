import { getAggregateAlias } from 'app/utils/discover/fields';
function HeaderCell(props) {
    var children = props.children, column = props.column, tableMeta = props.tableMeta;
    // establish alignment based on the type
    var alignedTypes = ['number', 'duration', 'integer', 'percentage'];
    var align = alignedTypes.includes(column.type) ? 'right' : 'left';
    if (column.type === 'never') {
        // fallback to align the column based on the table metadata
        var maybeType = tableMeta ? tableMeta[getAggregateAlias(column.name)] : undefined;
        if (maybeType !== undefined && alignedTypes.includes(maybeType)) {
            align = 'right';
        }
    }
    return children({ align: align });
}
export default HeaderCell;
//# sourceMappingURL=headerCell.jsx.map