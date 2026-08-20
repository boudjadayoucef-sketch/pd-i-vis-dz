import { initializeApp, getApps, getApp } from "firebase/app";
import { 
  initializeFirestore,
  persistentLocalCache,
  persistentMultipleTabManager,
  collection, 
  doc, 
  getDocs, 
  setDoc, 
  updateDoc, 
  deleteDoc, 
  addDoc 
} from "firebase/firestore";
import { getAuth } from "firebase/auth";
// Allow the user to override Firebase configuration via client-side environment variables
const metaEnv = (import.meta as any).env || {};

const defaultConfig = {
  apiKey: metaEnv.VITE_FIREBASE_API_KEY || "AIzaSy_demo_api_key_placeholder",
  authDomain: metaEnv.VITE_FIREBASE_AUTH_DOMAIN || "graphical-router-x18qq.firebaseapp.com",
  projectId: metaEnv.VITE_FIREBASE_PROJECT_ID || "graphical-router-x18qq",
  storageBucket: metaEnv.VITE_FIREBASE_STORAGE_BUCKET || "graphical-router-x18qq.firebasestorage.app",
  messagingSenderId: metaEnv.VITE_FIREBASE_MESSAGING_SENDER_ID || "757027531011",
  appId: metaEnv.VITE_FIREBASE_APP_ID || "1:757027531011:web:758a7df99506a6e9dc6136",
  firestoreDatabaseId: metaEnv.VITE_FIREBASE_DATABASE_ID || "ai-studio-remixpdi-12e4b2ec-ffc7-48b8-9472-8a77deb300cf"
};

const activeConfig = {
  apiKey: metaEnv.VITE_FIREBASE_API_KEY || defaultConfig.apiKey,
  authDomain: metaEnv.VITE_FIREBASE_AUTH_DOMAIN || defaultConfig.authDomain,
  projectId: metaEnv.VITE_FIREBASE_PROJECT_ID || defaultConfig.projectId,
  storageBucket: metaEnv.VITE_FIREBASE_STORAGE_BUCKET || defaultConfig.storageBucket,
  messagingSenderId: metaEnv.VITE_FIREBASE_MESSAGING_SENDER_ID || defaultConfig.messagingSenderId,
  appId: metaEnv.VITE_FIREBASE_APP_ID || defaultConfig.appId,
  firestoreDatabaseId: metaEnv.VITE_FIREBASE_DATABASE_ID || defaultConfig.firestoreDatabaseId
};

// Initialize Firebase
const app = getApps().length === 0 ? initializeApp(activeConfig) : getApp();

// Initialize Firestore with robust local offline persistence (IndexedDB)
const db = initializeFirestore(app, {
  localCache: persistentLocalCache({
    tabManager: persistentMultipleTabManager(),
  }),
}, activeConfig.firestoreDatabaseId || undefined);

const auth = getAuth(app);

export { db, auth, activeConfig };

// Interface for Plans (schemas)
export interface EngineeringPlan {
  id: string;
  title: string;
  fascicule: string;
  page: number;
  category: string;
  src: string;
  caption: string;
  tags: string[];
}

// Collection Names
const PLANS_COLLECTION = "plans";
const FASCICULES_COLLECTION = "fascicules_custom";

// --- Plans functions ---

// Fetch all plans
export async function fetchPlans(): Promise<EngineeringPlan[]> {
  try {
    const querySnapshot = await getDocs(collection(db, PLANS_COLLECTION));
    const plans: EngineeringPlan[] = [];
    querySnapshot.forEach((doc) => {
      plans.push({ id: doc.id, ...doc.data() } as EngineeringPlan);
    });
    return plans;
  } catch (error) {
    console.error("Error fetching plans from Firestore: ", error);
    throw error;
  }
}

// Add/Save plan
export async function savePlan(plan: Omit<EngineeringPlan, "id"> & { id?: string }): Promise<string> {
  try {
    if (plan.id) {
      await setDoc(doc(db, PLANS_COLLECTION, plan.id), plan);
      return plan.id;
    } else {
      const docRef = await addDoc(collection(db, PLANS_COLLECTION), plan);
      return docRef.id;
    }
  } catch (error) {
    console.error("Error saving plan to Firestore: ", error);
    throw error;
  }
}

// Delete plan
export async function deletePlanFromDb(id: string): Promise<void> {
  try {
    await deleteDoc(doc(db, PLANS_COLLECTION, id));
  } catch (error) {
    console.error("Error deleting plan from Firestore: ", error);
    throw error;
  }
}

// Seed plans if collection is empty
export async function seedPlansIfEmpty(defaultPlans: EngineeringPlan[]): Promise<void> {
  try {
    const querySnapshot = await getDocs(collection(db, PLANS_COLLECTION));
    if (querySnapshot.empty) {
      console.log("Seeding default plans into Firestore...");
      for (const plan of defaultPlans) {
        await setDoc(doc(db, PLANS_COLLECTION, plan.id), plan);
      }
    }
  } catch (error) {
    console.error("Error seeding plans: ", error);
  }
}

// Error handlers for standard formatting of Firestore Permission Errors
export enum OperationType {
  CREATE = 'create',
  UPDATE = 'update',
  DELETE = 'delete',
  LIST = 'list',
  GET = 'get',
  WRITE = 'write',
}

export interface FirestoreErrorInfo {
  error: string;
  operationType: OperationType;
  path: string | null;
  authInfo: {
    userId?: string | null;
    email?: string | null;
    emailVerified?: boolean | null;
    isAnonymous?: boolean | null;
    tenantId?: string | null;
    providerInfo?: {
      providerId?: string | null;
      email?: string | null;
    }[];
  }
}

export function handleFirestoreError(error: unknown, operationType: OperationType, path: string | null) {
  const errInfo: FirestoreErrorInfo = {
    error: error instanceof Error ? error.message : String(error),
    authInfo: {
      userId: auth.currentUser?.uid,
      email: auth.currentUser?.email,
      emailVerified: auth.currentUser?.emailVerified,
      isAnonymous: auth.currentUser?.isAnonymous,
      tenantId: auth.currentUser?.tenantId,
      providerInfo: auth.currentUser?.providerData?.map(provider => ({
        providerId: provider.providerId,
        email: provider.email,
      })) || []
    },
    operationType,
    path
  };
  console.error('Firestore Error: ', JSON.stringify(errInfo));
  throw new Error(JSON.stringify(errInfo));
}

export interface ProjectNotification {
  id?: string;
  projectId: string;
  projectName: string;
  message: string;
  category: "creation" | "update" | "assignment" | "status_change";
  authorName: string;
  authorEmail: string;
  authorRole?: string;
  timestamp: string;
  pole?: string;
  region?: string;
  readBy?: string[];
}

export async function createNotification(notif: Omit<ProjectNotification, "timestamp">): Promise<string> {
  try {
    const newNotif = {
      ...notif,
      timestamp: new Date().toISOString(),
      readBy: notif.readBy || []
    };
    const docRef = await addDoc(collection(db, "notifications"), newNotif);
    return docRef.id;
  } catch (error) {
    console.error("Error creating notification in Firestore:", error);
    throw error;
  }
}

