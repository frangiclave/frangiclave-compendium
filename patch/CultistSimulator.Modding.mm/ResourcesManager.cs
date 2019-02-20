using MonoMod;
using System.IO;
using Noon;
using UnityEngine;

#pragma warning disable CS0626

namespace CultistSimulator.Modding.mm
{
    [MonoModPatch("global::ResourcesManager")]
    public class ResourcesManager
    {
        public static extern Sprite orig_GetSpriteForVerbLarge(string verbId);

		public static Sprite GetSpriteForVerbLarge(string verbId)
		{
			return GetSprite("icons100/verbs/", verbId);
		}

	    public static extern Sprite orig_GetSpriteForElement(string imageName);

		public static Sprite GetSpriteForElement(string imageName)
		{
			return GetSprite("elementArt/", imageName);
		}

	    public static extern Sprite orig_GetSpriteForElement(string imageName, int animFrame);

		public static Sprite GetSpriteForElement(string imageName, int animFrame)
		{
			return GetSprite("elementArt/anim/", string.Concat(imageName, "_", animFrame));
		}

	    public static extern Sprite orig_GetSpriteForCardBack(string backId);

		public static Sprite GetSpriteForCardBack(string backId)
		{
			return GetSprite("cardBacks/", backId);
		}

	    public static extern Sprite orig_GetSpriteForAspect(string aspectId);

		public static Sprite GetSpriteForAspect(string aspectId)
		{
			return GetSprite("icons40/aspects/", aspectId);
		}

	    public static extern Sprite orig_GetSpriteForLegacy(string legacyImage);

		public static Sprite GetSpriteForLegacy(string legacyImage)
		{
			return GetSprite("icons100/legacies/", legacyImage);
		}

	    public static extern Sprite orig_GetSpriteForEnding(string endingImage);

		public static Sprite GetSpriteForEnding(string endingImage)
		{
			return GetSprite("endingArt/en/", endingImage);
		}

	    private static Sprite GetSprite(string folder, string file)
	    {
		    NoonUtility.Log("Loading " + folder + file);
		    // Check if a local image exists; if it does, load it first
		    string localPath = Application.streamingAssetsPath + "/" + folder + file + ".png";
		    if (File.Exists(localPath))
		    {
			    var fileData = File.ReadAllBytes(localPath);
			    var texture = new Texture2D(2, 2);
			    texture.LoadImage(fileData);
			    return Sprite.Create(
				    texture, new Rect(0.0f, 0.0f, texture.width, texture.height), new Vector2(0.5f, 0.5f));
		    }

		    // Try to load the image from the packed resources next, and show the placeholder if not found
		    Sprite sprite = Resources.Load<Sprite>(folder + file);
		    return sprite != null ? sprite : Resources.Load<Sprite>(folder + PLACEHOLDER_IMAGE_NAME);
	    }

	    private const string PLACEHOLDER_IMAGE_NAME = "_x";
    }
}
