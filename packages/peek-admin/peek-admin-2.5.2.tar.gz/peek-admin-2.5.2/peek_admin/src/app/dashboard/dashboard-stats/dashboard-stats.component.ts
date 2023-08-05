import { Component } from "@angular/core"
import { ComponentLifecycleEventEmitter, VortexService, VortexStatusService } from "@synerty/vortexjs"

interface Stat {
    desc: string
    value: string
}

@Component({
    selector: "app-dashboard-stats",
    templateUrl: "./dashboard-stats.component.html",
    styleUrls: ["./dashboard-stats.component.scss"]
})
export class DashboardStatsComponent extends ComponentLifecycleEventEmitter {
    // stats: Stat[] = []
    // loader: TupleLoader
  
    private readonly statsFilt = {
        plugin: "peek_server",
        key: "peakadm.dashboard.list.data"
    }
    
    constructor(
        vortexService: VortexService,
        vortexStatus: VortexStatusService
    ) {
        super()
        
        // this.loader = vortexService.createTupleLoader(this, this.statsFilt);
        //
        //
        // vortexStatus
        //   .isOnline
        //   .filter(online => online)
        //   .first()
        //   .subscribe(() => {
        //     this.loader.observable.subscribe(
        //       tuples => {
        //         this.stats = <Stat[]>tuples;
        //         this.stats.sort((a, b) => {
        //           return (<Stat>a).desc.localeCompare((<Stat>b).desc);
        //         });
        //       });
        //   });
    }
}
