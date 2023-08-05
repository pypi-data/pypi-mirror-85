import {addTupleType, Tuple} from "@synerty/vortexjs";
import {ChunkedTypeTuple} from "./ChunkedTypeTuple";
import {ChunkedIndexModelSetTuple} from "./ChunkedIndexModelSetTuple";


@addTupleType
export class ChunkedTuple extends Tuple {
    public static readonly tupleName = chunkedIndexTuplePrefix + "ChunkedTuple";

    //  The unique key of this chunkedIndex
    key: string;

    //  The modelSetId for this chunkedIndex.
    modelSet: ChunkedIndexModelSetTuple = new ChunkedIndexModelSetTuple();

    // This ChunkedIndex Type ID
    chunkedType: ChunkedTypeTuple = new ChunkedTypeTuple();

    // A string value of the chunked
    valueStr: string;

    // An int value of the chunked
    valueInt: number;

    // Add more values here

    constructor() {
        super(ChunkedTuple.tupleName)
    }

    static unpackJson(key: string, packedJson: string): ChunkedTuple {
        // Reconstruct the data
        let objectProps: {} = JSON.parse(packedJson);

        // Get out the object type
        let thisChunkedTypeId = objectProps['_tid'];
        delete objectProps['_tid'];

        // Get out the object type
        let thisModelSetId = objectProps['_msid'];
        delete objectProps['_msid'];

        // Create the new object
        let newSelf = new ChunkedTuple();

        newSelf.key = key;

        // These objects get replaced later in the UI
        newSelf.modelSet = new ChunkedIndexModelSetTuple();
        newSelf.modelSet.id__ = thisModelSetId;
        newSelf.chunkedType = new ChunkedTypeTuple();
        newSelf.chunkedType.id__ = thisChunkedTypeId;

        // Unpack the custom data here
        newSelf.valueStr = objectProps["valueStr"];
        newSelf.valueInt = objectProps["valueInt"];

        return newSelf;

    }
}