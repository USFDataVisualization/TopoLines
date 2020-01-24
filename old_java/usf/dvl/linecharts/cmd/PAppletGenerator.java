package usf.dvl.linecharts.cmd;

import java.util.ArrayList;
import java.util.HashSet;

import processing.core.PApplet;
import processing.data.JSONArray;
import processing.data.JSONObject;
import usf.dvl.common.TaskExecutorService;
import usf.dvl.common.TaskExecutorService.Task;
import usf.dvl.draw.frames.LineChartFrame;
import usf.dvl.linecharts.auto.FilterInstance;
import usf.dvl.processing.PFrameApplet;
import usf.dvl.topology.distance.HeraTopologicalDistance;

public class PAppletGenerator extends PFrameApplet<LineChartFrame> {
	
	
	TaskExecutorService exec = new TaskExecutorService(6);

	
	String outputBase = "/Users/prosen/datasets";
	String dbURI = "http://localhost:3500/admin/listing";

	public void setup(){
		super.setup();
		
		HeraTopologicalDistance.wasserstein_dist_path = "/Users/prosen/Code/usfdvl-topology/tda/hera/wasserstein_dist.mac";
		HeraTopologicalDistance.bottleneck_dist_path  = "/Users/prosen/Code/usfdvl-topology/tda/hera/bottleneck_dist.mac";
		//HeraTopologicalDistance.wasserstein_dist_path = "/home/prosen/topolines/wasserstein_dist.linux";
		//HeraTopologicalDistance.bottleneck_dist_path  = "/home/prosen/topolines/bottleneck_dist.linux";
		


		HashSet<String> processed = new HashSet<String>();
		JSONArray jsonTmp = this.loadJSONArray(dbURI);
		for( int i = 0; i < jsonTmp.size(); i++ ) {
			JSONObject json = jsonTmp.getJSONObject(i);
			String existing = json.getString( "datafile" ) + json.getString("filterType") + String.format("%.6f", json.getFloat("filterLevel") );
			processed.add( existing );
		}

		ArrayList<FilterInstance> work = new ArrayList<FilterInstance>();
		

		
		
		work.addAll( FilterInstance.procDataset( this, exec, "/climate/DroughtSevIndx1901_2000.json",100, new float[] {1.0f,   9.4f},  new float[] {1.1f, 30}, new float[] {1, 118}, new float[] {1, 30}, new float[] {0.5f, 15.0f}, new float[] {0.5f,   6.5f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/climate/avgTemp.json",				 100, new float[] {0.5f,   3.2f},  new float[] {1.1f, 30}, new float[] {1, 119}, new float[] {1, 30}, new float[] {0.5f, 20.0f}, new float[] {0.25f,  2.75f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/climate/contiguousPerception.json",	 100, new float[] {1.0f,   9.0f},  new float[] {1.1f, 20}, new float[] {1, 119}, new float[] {1, 20}, new float[] {0.25f,20.0f}, new float[] {0.5f,   4.9f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/climateData/t13-14.json",			 100, new float[] {0.5f,  20.0f},  new float[] {1.1f, 20}, new float[] {1, 360}, new float[] {1, 30}, new float[] {0.25f,15.0f}, new float[] {0.5f,  20.0f} ) ); 
		work.addAll( FilterInstance.procDataset( this, exec, "/climateData/t14-15.json",			 100, new float[] {0.5f,  20.0f},  new float[] {1.1f, 20}, new float[] {1, 360}, new float[] {1, 30}, new float[] {0.25f,15.0f}, new float[] {0.5f,  20.0f} ) ); 
		work.addAll( FilterInstance.procDataset( this, exec, "/climateData/t15-16.json",			 100, new float[] {0.5f,  20.0f},  new float[] {1.1f, 20}, new float[] {1, 364}, new float[] {1, 30}, new float[] {0.25f,15.0f}, new float[] {0.5f,  20.0f} ) ); 
		work.addAll( FilterInstance.procDataset( this, exec, "/climateData/t16-17.json",			 100, new float[] {0.5f,  20.0f},  new float[] {1.1f, 20}, new float[] {1, 360}, new float[] {1, 30}, new float[] {0.25f,15.0f}, new float[] {0.5f,  20.0f} ) ); 
		work.addAll( FilterInstance.procDataset( this, exec, "/climateData/t17-18.json",			 100, new float[] {0.5f,  20.0f},  new float[] {1.1f, 20}, new float[] {1, 357}, new float[] {1, 30}, new float[] {0.25f,15.0f}, new float[] {0.5f,  20.0f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/eeg/chan1.csv", 						 100, new float[] {1.0f, 110.0f},  new float[] {1.1f,100}, new float[] {1,1975}, new float[] {1,100}, new float[] {0.5f, 50.0f}, new float[] {0.5f, 110.0f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/eeg/chan7.csv", 						 100, new float[] {1.0f,  85.0f},  new float[] {1.1f,100}, new float[] {1,1975}, new float[] {1,100}, new float[] {0.5f, 50.0f}, new float[] {0.5f, 100.0f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/eeg/chan14.csv", 					 100, new float[] {1.0f, 120.0f},  new float[] {1.1f,100}, new float[] {1,1975}, new float[] {1,100}, new float[] {0.5f, 50.0f}, new float[] {0.5f, 100.0f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/eeg/chan21.csv", 					 100, new float[] {1.0f, 110.0f},  new float[] {1.1f,100}, new float[] {1,1975}, new float[] {1,100}, new float[] {0.5f, 50.0f}, new float[] {0.5f,  95.0f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/eeg/chan28.csv", 					 100, new float[] {1.0f, 110.0f},  new float[] {1.1f,100}, new float[] {1,1975}, new float[] {1,100}, new float[] {0.5f, 50.0f}, new float[] {0.5f,  95.0f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/radioAstronomy/output_115_119.json",  100, new float[] {0.001f, 0.1f},  new float[] {2.0f, 30}, new float[] {1,1939}, new float[] {1, 15}, new float[] {0.25f,10.0f}, new float[] {0.001f, 0.1f} ) ); 
		work.addAll( FilterInstance.procDataset( this, exec, "/radioAstronomy/output_115_130.json",  100, new float[] {0.001f, 0.1f},  new float[] {2.0f, 30}, new float[] {1,1939}, new float[] {1, 15}, new float[] {0.25f,10.0f}, new float[] {0.001f, 0.1f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/radioAstronomy/output_116_133.json",  100, new float[] {0.001f, 0.05f}, new float[] {2.0f, 30}, new float[] {1,1939}, new float[] {1, 15}, new float[] {0.25f,10.0f}, new float[] {0.001f, 0.1f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/radioAstronomy/output_117_121.json",  100, new float[] {0.001f, 0.1f},  new float[] {2.0f, 30}, new float[] {1,1939}, new float[] {1, 15}, new float[] {0.25f,10.0f}, new float[] {0.001f, 0.1f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/radioAstronomy/output_119_123.json",  100, new float[] {0.001f, 0.1f},  new float[] {2.0f, 30}, new float[] {1,1939}, new float[] {1, 15}, new float[] {0.25f,10.0f}, new float[] {0.001f, 0.1f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/stock/amzn.json",					 100, new float[] {0.5f,  65.0f},  new float[] {1.1f, 35}, new float[] {1, 294}, new float[] {1, 30}, new float[] {0.5f,  9.5f}, new float[] {0.5f,  85.0f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/stock/appl.json",					 100, new float[] {0.5f,  24.0f},  new float[] {1.1f, 35}, new float[] {1, 294}, new float[] {1, 30}, new float[] {0.5f,  9.5f}, new float[] {0.5f,  19.75f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/stock/googl.json",					 100, new float[] {0.5f, 100.0f},  new float[] {1.1f, 35}, new float[] {1, 310}, new float[] {1, 30}, new float[] {0.5f,  9.5f}, new float[] {0.5f, 100.0f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/stock/intc.json",					 100, new float[] {0.5f,   7.3f},  new float[] {1.1f, 35}, new float[] {1, 310}, new float[] {1, 30}, new float[] {0.5f,  9.5f}, new float[] {0.5f,   6.75f} ) );
		work.addAll( FilterInstance.procDataset( this, exec, "/stock/msft.json",					 100, new float[] {0.5f,  10.0f},  new float[] {1.1f, 35}, new float[] {1, 310}, new float[] {1, 30}, new float[] {0.5f,  9.5f}, new float[] {0.5f,   6.2f} ) );

		

		
		for( FilterInstance inst : work ) {
			
			String curr = inst.dataFile + inst.filterType + String.format("%.6f", inst.filterLevel );
			if( !processed.contains( curr ) ) {
				exec.submitTask(inst);
			}	
			//if( exec.getTotalTasks() > 10 ) break; 
		}

		int recordsPerFile = 250;
		int curDS = 0;
		if( exec.getTotalTasks() > 0 ) {
			System.out.println("processing...");
			exec.shutdown(false);
			while( !exec.isTermintated(1) ) {
				System.out.println( (curDS*recordsPerFile+exec.getCompletedTasks().size()) + " of " + exec.getTotalTasks() + " completed of " + work.size() );
				if( exec.getCompletedTasks().size() > recordsPerFile ) {
					saveBatch( curDS++, recordsPerFile );
				}
			}			
			saveBatch( curDS++, exec.getCompletedTasks().size() );
			//exec.forceShutdown();
		}
		System.out.println("exec complete");

	}
	

	private void saveBatch( int curDS, int batchSize ) {
		JSONArray json = new JSONArray();
		ArrayList<Task> saved = new ArrayList<Task>();
		for( int i = 0; i < batchSize && i < exec.getCompletedTasks().size(); i++ ) {
			FilterInstance t = (FilterInstance)exec.getCompletedTasks().get(i);
			saved.add(t);
			if( !t.success() ) continue;
			json.append( t.toJSON() );
		}
		this.saveJSONArray(json, outputBase + curDS + ".json" );
		System.out.println("Saved: " + outputBase + curDS + ".json");
		exec.getCompletedTasks().removeAll(saved);
	}
	
	@Override public void draw() { exit(); }
	

	

		

	public PAppletGenerator() { super( 1200, 700, true ); }

	public static void main(String args[]) {
		PApplet.main(new String[] { "usf.dvl.linecharts.cmd.PAppletGenerator" });
	}


}
