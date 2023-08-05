import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {BranchDetailTuple, branchBaseUrl} from "@peek/peek_plugin_branch/_private";

import {
    ComponentLifecycleEventEmitter,
    TupleDataObserverService,
    TupleSelector
} from "@synerty/vortexjs";

import {TupleActionPushService} from "@synerty/vortexjs";

import {
    CreateBranchActionTuple
} from "@peek/peek_plugin_branch/_private";


@Component({
    selector: 'plugin-branch-branch-detail',
    templateUrl: 'branch-detail.component.mweb.html',
    moduleId: module.id
})
export class BranchDetailComponent extends ComponentLifecycleEventEmitter {

    branchDetails: Array<BranchDetailTuple> = [];

    constructor(private actionService: TupleActionPushService,
                private tupleDataObserver: TupleDataObserverService,
                private router: Router) {
        super();

        // // Create the TupleSelector to tell the observable what data we want
        // let selector = {};
        // // Add any filters of the data here
        // // selector["lookupName"] = "brownCowList";
        // let tupleSelector = new TupleSelector(BranchDetailTuple.tupleName, selector);
        //
        // // Setup a subscription for the data
        // let sup = tupleDataObserver.subscribeToTupleSelector(tupleSelector)
        //     .subscribe((tuples: BranchDetailTuple[]) => {
        //         // We've got new data, assign it to our class variable
        //         this.branchDetails = tuples;
        //     });
        //
        // // unsubscribe when this component is destroyed
        // // This is a feature of ComponentLifecycleEventEmitter
        // this.onDestroyEvent.subscribe(() => sup.unsubscribe());

    }

    mainClicked() {
        this.router.navigate([branchBaseUrl]);
    }

}