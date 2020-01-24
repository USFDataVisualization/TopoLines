package usf.dvl.signal;

import java.io.File;
import java.io.PrintWriter;

import usf.dvl.common.SystemX;

public class SignalFFT extends Signal {

	private static String pythonScriptPath = null;

	public SignalFFT( Signal graph ) {
		super( graph );
				
		String result="";
		try {
			File pythonDataPath = File.createTempFile( "pnt_", ".txt" );
			pythonDataPath.deleteOnExit();

			PrintWriter pw = new PrintWriter( pythonDataPath );
			for (int i =0; i<graph.size(); i++) {
				pw.println(String.valueOf(graph.get(i)));
			}
			pw.close();
			
			if( pythonScriptPath == null ) {
				pythonScriptPath = SystemX.getResourceFile( "/" + SignalFFT.class.getPackage().getName().replace(".", "/"), "rfft.py" ).getAbsolutePath();
				//System.out.println( pythonScriptPath );
			}
			
			String cmd = "python " + pythonScriptPath + " " + pythonDataPath;
			result = SystemX.executeCommand( cmd );

			String[] results = result.trim().split("\\s+");

			for (String a : results) {
				if ( a != null && !a.isEmpty() ) {
					if( !a.equalsIgnoreCase("nan") ) 
						//addPoint( Float.NaN );
						//addPoint( 0 );
					//else
						addPoint( Math.abs( ( Float.valueOf( a ) ) ) );
				}
			} 			
		} catch (Exception e) {
			e.printStackTrace();
			System.out.println("result: " + result);
		}

	}

}


