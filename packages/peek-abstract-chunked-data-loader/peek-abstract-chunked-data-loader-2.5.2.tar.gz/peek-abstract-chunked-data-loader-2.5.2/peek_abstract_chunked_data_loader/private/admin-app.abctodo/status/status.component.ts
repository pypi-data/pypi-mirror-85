import {Component} from "@angular/core";
import {
    ComponentLifecycleEventEmitter,
    TupleDataObserverService,
    TupleSelector
} from "@synerty/vortexjs";
import { BalloonMsgService } from "@synerty/peek-plugin-base-js"
import {LoaderStatusTuple} from "../tuples/LoaderStatusTuple";


@Component({
    selector: 'pl-pof-diagram-loader-loader-status',
    templateUrl: './status.component.html'
})
export class StatusComponent extends ComponentLifecycleEventEmitter {

    item: LoaderStatusTuple = new LoaderStatusTuple();

    constructor(private balloonMsg: BalloonMsgService,
                private tupleObserver: TupleDataObserverService) {
        super();

        let sub = this.tupleObserver.subscribeToTupleSelector(
            new TupleSelector(LoaderStatusTuple.tupleName, {})
        ).subscribe((tuples: LoaderStatusTuple[]) => {
            this.item = tuples[0];
        });
        this.onDestroyEvent.subscribe(() => sub.unsubscribe());

    }


}
