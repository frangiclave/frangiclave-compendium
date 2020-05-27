using System;
using System.Collections.Generic;
using MonoMod;
using System.IO;
using System.Linq;
using Assets.Core.Entities;
using Noon;
using UnityEngine;

#pragma warning disable CS0626

namespace CultistSimulator.Modding.mm
{
    [MonoModPatch("global::SplashAnimation")]
    public class SplashAnimation
    {
        private extern void orig_Start();

        private void Start()
        {
            orig_Start();
            string path = Application.persistentDataPath + "/config.ini";
            string text = File.ReadAllText(path);
            if (!text.Contains("export=1"))
            {
                return;
            }
	        ExportAssetsToFileSystem();
        }

        private static void ExportAssetsToFileSystem()
		{
			// Export art
			LanguageTable.LoadCulture("en");
			ExportSpriteFolderToFileSystem("burnImages/", "png");
			ExportSpriteFolderToFileSystem("cardBacks/",  "png");
			ExportSpriteFolderToFileSystem("elementArt/", "png");
			ExportSpriteFolderToFileSystem("elementArt/anim/", "png");
			ExportSpriteFolderToFileSystem("endingArt/", "png");
			ExportSpriteFolderToFileSystem("icons40/aspects/", "png");
			ExportSpriteFolderToFileSystem("icons100/legacies/", "png");
			ExportSpriteFolderToFileSystem("icons100/verbs/", "png");
		}

		private static void ExportSpriteFolderToFileSystem(string sourceFolder, string ext)
		{
			string exportFolder = Path.Combine(ExportDir, sourceFolder);
			Directory.CreateDirectory(exportFolder);
			var encounteredNames = new HashSet<string>();
			foreach (var asset in Resources.LoadAll<Sprite>(sourceFolder))
			{
				NoonUtility.Log("Asset: " + asset.name);
				if (encounteredNames.Contains(asset.name))
				{
					NoonUtility.Log("Encountered before!");
					continue;
				}

				encounteredNames.Add(asset.name);
				string exportPath = Path.Combine(exportFolder, asset.name + "." + ext);
				File.WriteAllBytes(exportPath, GetSpriteAsPng(asset));
				Resources.UnloadAsset(asset);
			}
		}

		private static byte[] GetSpriteAsPng(Sprite sprite)
		{
			// Copy the texture so that its data can be manipulated
			// Source: https://support.unity3d.com/hc/en-us/articles/206486626-How-can-I-get-pixels-from-unreadable-textures-
			RenderTexture tmp = RenderTexture.GetTemporary(
				sprite.texture.width,
				sprite.texture.height,
				0,
				RenderTextureFormat.Default,
				RenderTextureReadWrite.Linear);
			Graphics.Blit(sprite.texture, tmp);
			RenderTexture previous = RenderTexture.active;
			RenderTexture.active = tmp;
			Texture2D spriteTexture = new Texture2D(sprite.texture.width, sprite.texture.height);
			spriteTexture.ReadPixels(new Rect(0, 0, tmp.width, tmp.height), 0, 0);
			spriteTexture.Apply();
			RenderTexture.active = previous;
			RenderTexture.ReleaseTemporary(tmp);

			// Crop the texture to the sprite
			Rect r = sprite.textureRect;
			Texture2D croppedTextured = spriteTexture.CropTexture((int) r.x, (int) r.y, (int) r.width, (int) r.height);
			return croppedTextured.EncodeToPNG();
		}

	    private static readonly string ExportDir = Application.streamingAssetsPath;
    }
}
