import {Injectable} from "@angular/core";

import {
    ComponentLifecycleEventEmitter,
    Payload,
    TupleActionPushService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleSelector,
    VortexStatusService
} from "@synerty/vortexjs";

import {Subject} from "rxjs/Subject";
import {Observable} from "rxjs/Observable";
import {ChunkedIndexResultI, ChunkedIndexLoaderService} from "./_private/chunked-index-loader";

// ----------------------------------------------------------------------------
/** ChunkedIndex Cache
 *
 * This class has the following responsibilities:
 *
 * 1) Maintain a local storage of the index
 *
 * 2) Return DispKey locations based on the index.
 *
 */
@Injectable()
export class ChunkedIndexService extends ComponentLifecycleEventEmitter {


    constructor(private chunkedIndexLoader: ChunkedIndexLoaderService) {
        super();

    }

    /** Get Chunkeds
     *
     * Get the objects for key from the index..
     *
     */
    getChunkeds(modelSetKey: string, keys: string[]): Promise<ChunkedIndexResultI> {
        return this.chunkedIndexLoader.getChunkeds(modelSetKey, keys);
    }

}