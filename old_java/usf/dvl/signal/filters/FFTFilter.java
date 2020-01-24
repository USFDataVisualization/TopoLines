package usf.dvl.signal.filters;

import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;

import usf.dvl.common.SystemX;
import usf.dvl.signal.Signal;

public class FFTFilter extends FilteredSignal {

	private static String pythonScriptPath = null;


	
	//int minF, maxF;

	public FFTFilter( Signal graph, int fCut ) {
		super( graph, fCut );

		try {
			File pythonDataPath = File.createTempFile( "pnt_", ".txt" );
			pythonDataPath.deleteOnExit();
			//System.out.println(pythonDataPath.getAbsolutePath() );
			
			PrintWriter pw = new PrintWriter( pythonDataPath );
			for (int i =0; i < graph.size(); i++) {
				pw.println( String.valueOf( graph.get(i) ) );
			}
			pw.close();
			
			if( pythonScriptPath == null ) {
				pythonScriptPath = SystemX.getResourceFile( "/" + FFTFilter.class.getPackage().getName().replace(".", "/"), "lowpass.py" ).getAbsolutePath();
				//System.out.println( pythonScriptPath );
			}

			int tFreq = graph.size();
			String cmd = "python " + pythonScriptPath + " " + pythonDataPath + " " + 0 + " " + (tFreq-fCut);
			String result = SystemX.executeCommand( cmd );

			String[] results = result.trim().split("\\s+");

			for (String a : results) {
				if ( a != null && !a.isEmpty() ) {
					addPoint( Float.valueOf( a ) );
				}
			} 			
		} catch (IOException e) {
			e.printStackTrace();
		}

	}

	@Override public String graphType( ) {
		return filterType();
	}
	
	public static String filterType( ) {
		return "Low-Pass";
	}
	
}


