package com.example.test01;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import org.opencv.android.BaseLoaderCallback;
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCamera2View;
import org.opencv.android.JavaCameraView;
import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.imgproc.Imgproc;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {

    ImageView img1;
    Uri imageUri;
    Bitmap grayBitmap, imageBitmap;
    Button btnGallery, btnGray;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        OpenCVLoader.initDebug();
        img1 = (ImageView) findViewById(R.id.img_test);
        btnGallery = findViewById(R.id.btn_gallery);
        btnGray = findViewById(R.id.btn_gray);
        btnGallery.setOnClickListener(v -> openGallery());
        btnGray.setOnClickListener(v -> convertToGray());

    }

    public void openGallery() {
        Intent myIntent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        startActivityForResult(myIntent, 100);
    }

    public void convertToGray() {
        Mat Rgba = new Mat();
        Mat grayMat = new Mat();

        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inDither = false;
        options.inSampleSize = 4;

        int width = imageBitmap.getWidth();
        int heght = imageBitmap.getHeight();

        grayBitmap = Bitmap.createBitmap(width, heght, Bitmap.Config.RGB_565);

        //bitmap -> MAT:
        Utils.bitmapToMat(imageBitmap, Rgba);
        Imgproc.cvtColor(Rgba, grayMat, Imgproc.COLOR_RGB2GRAY);
        //Mat -> bitmap :
        Utils.matToBitmap(grayMat, grayBitmap);

        img1.setImageBitmap(grayBitmap);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == 100 && resultCode == RESULT_OK && data != null) {
            Uri imageUri = data.getData();
            try {
                imageBitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), imageUri);
            } catch (IOException e) {
                e.printStackTrace();
            }
            img1.setImageBitmap(imageBitmap);

        }
    }
}