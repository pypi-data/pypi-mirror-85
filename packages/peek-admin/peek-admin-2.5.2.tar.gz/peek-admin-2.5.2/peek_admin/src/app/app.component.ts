import { Component, OnInit } from "@angular/core"
import { VortexService } from "@synerty/vortexjs"

@Component({
    selector: "app-root",
    templateUrl: "./app.component.html",
    styleUrls: ["./app.component.scss"]
})
export class AppComponent implements OnInit {
    
    constructor(private vortexService: VortexService) { }
    
    ngOnInit() {
        // This causes two reconnections when the app starts
        // this.vortexService.reconnect();
    }
}
