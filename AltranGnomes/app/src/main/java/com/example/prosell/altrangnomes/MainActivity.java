package com.example.prosell.altrangnomes;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.AsyncTask;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.method.LinkMovementMethod;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        new GnomeRequest(this).execute("api_data");



        final Button imagesButton = (Button) findViewById(R.id.imagesButton);
        imagesButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                String url = "https://www.dropbox.com/sh/nen6hh47z4wh8cp/AAAJv8lY4w9wChJdnuhC1t9Ta?dl=0";

                Intent i = new Intent(Intent.ACTION_VIEW);
                i.setData(Uri.parse(url));
                startActivity(i);
            }
        });
        //LIGHT CONTROLS
        final Button turnOnLights = (Button) findViewById(R.id.lightOn);
        turnOnLights.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                new GnomeRequest(v.getContext()).execute("turnOnLights");
                // Perform action on click
            }
        });

        final Button turnOffLights = (Button) findViewById(R.id.lightOff);
        turnOffLights.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                new GnomeRequest(v.getContext()).execute("turnOffLights");
                // Perform action on click
            }
        });

        final Button setAutoLights = (Button) findViewById(R.id.lightAuto);
        setAutoLights.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                new GnomeRequest(v.getContext()).execute("setAutoLights");
                // Perform action on click
            }
        });

        //FAN CONTROLS
        final Button turnOnFan = (Button) findViewById(R.id.fanOn);
        turnOnFan.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                new GnomeRequest(v.getContext()).execute("turnOnFan");
                // Perform action on click
            }
        });

        final Button turnOffFan = (Button) findViewById(R.id.fanOff);
        turnOffFan.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                new GnomeRequest(v.getContext()).execute("turnOffFan");
                // Perform action on click
            }
        });

        final Button setAutoFan = (Button) findViewById(R.id.fanAuto);
        setAutoFan.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                new GnomeRequest(v.getContext()).execute("setAutoFan");
                // Perform action on click
            }
        });



        final Button takePicture = (Button) findViewById(R.id.CaptureButton);
        takePicture.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                new GnomeRequest(v.getContext()).execute("take_picture");
                // Perform action on click
            }
        });


    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.ipConfig){
            Intent settingsActivity = new Intent(this,SettingsActivity.class);
            startActivity(settingsActivity);
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    private class GnomeRequest extends AsyncTask<String, Integer, String> {

        private HttpURLConnection urlConnection;
        private Context mContext;

        public GnomeRequest(Context context){
            mContext = context;
        }

        @Override
        protected String doInBackground(String... args) {

            StringBuilder result = new StringBuilder();

            String function = args[0];

            SharedPreferences sharedPref = PreferenceManager.getDefaultSharedPreferences(mContext);
            String ip = sharedPref.getString(getString(R.string.ip), getString(R.string.ipDefault));
            try {
                URL url = new URL("http://" + ip + ":5000/" + function);
                urlConnection = (HttpURLConnection) url.openConnection();
                InputStream in = new BufferedInputStream(urlConnection.getInputStream());

                BufferedReader reader = new BufferedReader(new InputStreamReader(in));

                String line;
                while ((line = reader.readLine()) != null) {
                    result.append(line);
                }

            }catch( Exception e) {
                e.printStackTrace();
            }
            finally {
                urlConnection.disconnect();
            }


            return result.toString();
        }

        @Override
        protected void onPostExecute(String result) {

            //TextView textView = (TextView)findViewById(R.id.json_data);
            //System.out.println(textView);
            //textView.setText(result);
            //Do something with the JSON string

        }

    }
}
