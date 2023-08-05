import {addTupleType, Tuple} from "@synerty/vortexjs";


@addTupleType
export class ChunkedIndexUpdateDateTuple extends Tuple {
    public static readonly tupleName = chunkedIndexTuplePrefix + "ChunkedIndexUpdateDateTuple";

    // Improve performance of the JSON serialisation
    protected _rawJonableFields = ['initialLoadComplete', 'updateDateByChunkKey'];

    initialLoadComplete: boolean = false;
    updateDateByChunkKey: {} = {};

    constructor() {
        super(ChunkedIndexUpdateDateTuple.tupleName)
    }
}