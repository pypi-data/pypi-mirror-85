import {Component, OnInit} from "@angular/core";
import {
    VortexService,
    ComponentLifecycleEventEmitter,
    TupleLoader,
    Tuple,
    extend
} from "@synerty/vortexjs";
import {inboxFilt} from "@peek/peek_plugin_inbox/plugin-inbox-names";


class SettingProperty extends Tuple {

    id: number;
    settingId: number;
    key: string;
    type: string;

    int_value: number;
    char_value: string;
    boolean_value: boolean;

    constructor() {
        super('c.s.p.setting.property')
    }
}

@Component({
    selector: 'pl-inbox-setting-list',
    templateUrl: './admin-setting-list.component.html'
})
export class AdminSettingListComponent extends ComponentLifecycleEventEmitter implements OnInit {
    private readonly filt = extend({
        key: "server.setting.data"
    },inboxFilt );

    items: SettingProperty[] = [];

    loader: TupleLoader;

    constructor(vortexService: VortexService) {
        super();

        this.loader = vortexService.createTupleLoader(this, this.filt);

        this.loader.observable.subscribe(
            tuples => this.items = <SettingProperty[]>tuples);
    }

    ngOnInit() {
    }

}
